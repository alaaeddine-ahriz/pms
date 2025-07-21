import os
import json
from typing import Optional

TOKEN_PATH = os.path.expanduser("~/.pms_cli_token")

def save_token(token: str):
    with open(TOKEN_PATH, "w") as f:
        json.dump({"access_token": token}, f)

def load_token() -> Optional[str]:
    if not os.path.exists(TOKEN_PATH):
        return None
    with open(TOKEN_PATH, "r") as f:
        data = json.load(f)
        return data.get("access_token")

def clear_token():
    if os.path.exists(TOKEN_PATH):
        os.remove(TOKEN_PATH)

def get_auth_header(token: Optional[str] = None):
    if not token:
        token = load_token()
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {} 