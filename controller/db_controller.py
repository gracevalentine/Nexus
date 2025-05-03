import redis
import json
from model.Account import Account
from model.AccountStatus import AccountStatus

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def save_account(account: Account):
    key = f"account:{account.id}"
    data = {
        "name": account.name,
        "password": account.password,
        "status": account.status.value  # Pastikan ini menyimpan nama status dengan benar
    }
    r.set(key, json.dumps(data))

def load_account(account_id):
    key = f"account:{account_id}"
    data = r.get(key)
    if data:
        data = json.loads(data)
        acc = Account(data["name"], data["password"], account_id)
        
        # Menambahkan pengecekan status agar tidak error jika tidak valid
        try:
            acc.status = AccountStatus[data["status"]]  # Pastikan ini mengembalikan status sesuai enum
        except KeyError:
            acc.status = AccountStatus.ACTIVE  # Jika status tidak valid, set default ke ACTIVE
            
        return acc
    return None
