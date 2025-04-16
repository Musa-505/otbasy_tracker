import json
from pathlib import Path

USERS_FILE = Path("data/users.json")

def save_user(chat_id: int):
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if USERS_FILE.exists():
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)
    else:
        users = []

    if chat_id not in users:
        users.append(chat_id)
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f)

def get_all_users() -> list[int]:
    if not USERS_FILE.exists():
        return []
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)