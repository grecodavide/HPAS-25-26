from flask import Request

# behave like a dict with extra fields
class State(dict[str, str]):
    wrong_credentials: bool =  False

    def __init__(self):
        super(State, self).__init__()

    def add(self, req: Request, fields: list[str]):
        for field in fields:
            value = req.form[field]
            assert type(value) == str
            self[field] = value
