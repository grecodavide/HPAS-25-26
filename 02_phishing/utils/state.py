from typing import override
from flask import Request

class State:
    username: str = ""
    password: str = ""
    wrong_credentials: bool = False

    @override
    def __repr__(self):
        return "=======================\nUsername: {username}, password: {password}. They are {correct}\n=======================".format(
                username = self.username,
                password = self.password,
                correct = "WRONG" if self.wrong_credentials else "CORRECT"
        )

    def assign(self, req: Request):
        assert type(req.form["username"]) == str
        assert type(req.form["password"]) == str

        self.username = req.form["username"]
        self.password = req.form["password"]


