# How to run
First, create a venv and enter it:
```sh
python -m venv .venv
source ./.venv/bin/activate
```
Then, install needed packages:

```sh
pip install -r requirements.txt
```

Finally:
```sh
flask run # to just see
flask --debug run # to work on (reload works)
```

# Paths changes
## In templates
In templates, paths become "{{url_for('static', filename='')}}"

## In css files
In css we just remove paths and keep names, if all in the same folder (`<resource>`)

## In js
In js we just put the relative path after rendering (`/static/<folder>/<resource>`)

# Flow of events
## Login with credentials
1. User enters the website
2. he clicks on "login with CIE"
3. he is redirected to `do_login`
4. server clicks on "login with CIE", getting the actual HTML
5. user gets redirected to `cie_login`
6. he enters his credentials
7. he clicks "Procedi"
8. he is redirected to `receive`
9. server fills in user credentials
10. server clicks "Procedi"
11. server processses the answer: if it is positive, redirects user to `cie_waiting_push`, otherwise redirects user to `cie_wrong_credentials`, where the behavior is the same of point 8 but with a slightly different HTML
.... (TO BE DEFINED)

## Login with QR
1. User enters the website
2. he clicks on "login with CIE"
3. he is redirected to `do_login`
4. server clicks on "login with CIE", getting the actual HTML
5. user gets redirected to `cie_login`, which will contain the QR and challenge from the actual HTML received in point 4.
6. he scans the qr
