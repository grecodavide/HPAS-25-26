from utils.state import State


def perform_login_up(state: State):
    s = f"username is '{state['username']}', password is '{state['password']}'"
    sep = "=" * len(s)
    print(sep + "\n" + s + "\n" + sep)
