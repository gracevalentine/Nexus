from model.AccountStatus import AccountStatus
from model.Gamers import Gamers
from model.Admin import Admin
from model.Publisher import Publisher
from controller.db_controller import r
import json


def get_account(username: str, password: str):
    # Cek semua key dengan prefix 'account:'
    for key in r.scan_iter("account:*"):
        data_json = r.get(key)
        if not data_json:
            continue
        data = json.loads(data_json)

        # Cocokkan username dan password
        if data["name"] == username and data["password"] == password:
            role = data.get("role", "GAMER")  # Default ke GAMER jika tidak ada
            status = AccountStatus[data.get("status", "ACTIVE")]
            account_id = int(key.split(":")[1])

            # Pembentukan objek berdasarkan role
            if role == "GAMER":
                gamer = Gamers(data["name"], data["password"], account_id)
                gamer.set_status(status)
                gamer.set_wallet(data.get("wallet", 0.0))
                gamer.set_games(data.get("games", []))
                gamer.set_dlcs(data.get("dlcs", []))
                return gamer

            elif role == "ADMIN":
                admin = Admin(data["name"], data["password"], account_id)
                admin.set_status(status)
                return admin

            elif role == "PUBLISHER":
                publisher = Publisher(data["name"], data["password"], account_id)
                publisher.set_status(status)
                publisher.set_published_games(data.get("published_games", []))
                publisher.set_published_dlcs(data.get("published_dlcs", []))
                return publisher

    return None
