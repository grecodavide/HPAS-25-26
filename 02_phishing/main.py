from flask import Flask

app = Flask(__name__)

@app.route("/")
def main_page():
    return "<p>Hello world!</p>"

@app.route("/login")
def login():
    return "<p>This is the login page</p>"
