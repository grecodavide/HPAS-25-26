from utils.state import State

def perform_login_up(state: State):
    print(f"===========================================\nReceived username '{state["username"]}' and password '{state["password"]}'\n===========================================")
