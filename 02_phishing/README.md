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
flask run         [firefox]  # to just see
flask --debug run [firefox]  # to work on (reload works)
```

If the `firefox` argument is passed, the scraper will use firefox to perform the actual login.
Note that firefox does not support `detach` option, so when the server gets shut down, the browser session will be closed.

# Paths changes
## In templates
In templates, paths become "{{url_for('static', filename='')}}"

## In css files
In css we just remove paths and keep names, if all in the same folder (`<resource>`)

## In js
In js we just put the relative path after rendering (`/static/<folder>/<resource>`)


# Flow of execution
1. User clicks email link, getting redirected to our site
2. User clicks on "login with CIE" button, getting redirected to `/do_login`
3. In `/do_login`, we perform the actual login, retrieve the elements we need, and redirect the user to `/idp/login/livello2/` (same url of the original website)
4. Since we set the `challenge` argument in the url, we know we have to display the login screen
5. From there, we have two different flows: UP + push notification, or QR code

## UP and push notification
1. User inserts credentials, then clicks "Proceed" button, getting redirected to `/idp/login/livello2/` without the `challenge` argument, so we know we have to handle something else (in this case, UP and push login). The `username` and `password` fields are non-empty only the first time we perform login.
2. The scraper inserts the credentials in the actual website, and clicks the "Proceed" button.
If a successful response is received, it then shows the user the "waiting for push notification" screen
3. If the user clicks on the notification, we get redirected to the approval page on the scraper and then we show the user an error page
If the user inserts wrong credentials, we redirect them to the same url without any of `username`, `password`, and `challenge` so that we know the user inserted wrong credentials

## QR code
The QR code gets retrieved from the actual website, so as soon as the user lands on the page the periodic check starts. If the user scans it, we immediately skip over and show the error page to him getting the actual session
