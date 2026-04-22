from flask import Flask, render_template

app = Flask(__name__)

# TODO: translation, footer, background image

@app.route('/')
def home():
    return render_template('landing_page.html')

@app.route('/en')
def home_en():
    return render_template('landing_page_en.html')

@app.route('/AuthRequestCieService')
def cie_login():
    return ""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
