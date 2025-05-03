import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def save_account(account):
    key = f"account:{account.id}"
    data = {
        "name": account.name,
        "password": account.password,
        "status": account.status.name
    }
    r.set(key, json.dumps(data))

def load_account(account_id):
    key = f"account:{account_id}"
    data = r.get(key)
    if data:
        data = json.loads(data)
        from account import Account, AccountStatus
        acc = Account(data["name"], data["password"], account_id)
        acc.status = AccountStatus[data["status"]]
        return acc
    return None