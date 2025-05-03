import json
from db_controller import r
from model.Gamers import Gamers as gamers
from model.Account import Account, Role
from model.Publisher import Publisher as publisher

def insert_new_account(account: Account, role: Role):
    key = f"account:{account.id}"
    if r.exists(key):
        return False  # Account sudah ada

    if account.role == Role.GAMER:
        data = {
            "id": account.id,
            "name": account.name,
            "password": account.password,
            "role": role.GAMER,
            "wallet": gamers.get_wallet(account),
            "games": gamers.get_games(account),
            "dlcs": gamers.get_dlcs(account)
        }
    elif account.role == Role.ADMIN:
        data = {
            "id": account.id,
            "name": account.name,
            "password": account.password,
            "role": role.ADMIN
        }
    elif account.role == Role.PUBLISHER:
        data = {
            "id": account.id,
            "name": account.name,
            "password": account.password,
            "role": role.PUBLISHER,
            "published_games": publisher.get_published_games(account),
            "published_dlcs": publisher.get_published_dlcs(account)
        }
    else:
        return False  # Role tidak valid

    r.set(key, json.dumps(data))
    return True

def get_account_by_name_and_password(name, password):
    for key in r.scan_iter("account:*"):
        data = json.loads(r.get(key))
        if data["name"] == name and data["password"] == password:
            role = data["role"]
            if role == "GAMER":
                acc = gamers(data["name"], data["password"], data["id"])
                acc.set_wallet(data["wallet", 0.0])
                acc.set_games(data.get("games", []))
                acc.set_dlcs(data.get("dlcs", []))
                return acc
            else:
                acc = Account(data["name"], data["password"], data["id"])
                acc.set_role(Role[role])
                return acc
    return None

def update_wallet(account, top_up_amount):
    if account != Role.GAMER:
        return False  # Hanya gamer yang punya wallet

    key = f"account:{account.id}"
    data = r.get(key)
    if not data:
        return False

    data = json.loads(data)
    current_wallet = data.get("wallet", 0.0)
    updated_wallet = current_wallet + top_up_amount
    data["wallet"] = updated_wallet
    r.set(key, json.dumps(data))

    account.set_wallet(updated_wallet)
    return True
