from flask import Request

class State(dict[str, str]):
    wrong_credentials: bool

    def __init__(self):
        super(State, self).__init__()
        self.wrong_credentials = False

    def add(self, req: Request, fields: list[str]):
        for field in fields:
            value = req.form[field]
            assert type(value) == str
            self[field] = value
