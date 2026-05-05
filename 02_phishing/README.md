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
