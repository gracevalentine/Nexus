from shared.database import get_db_connection
from authentication.model.Gamer import Gamer
from authentication.model.Role import Role
from authentication.model.AccountStatus import AccountStatus

def get_wallet_balance(gamer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT balance FROM gamer_wallet WHERE account_id = %s', (gamer_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return result[0] if result else None

def topup_wallet(gamer_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Ambil saldo sekarang
    cursor.execute('SELECT balance FROM gamer_wallet WHERE account_id = %s', (gamer_id,))
    result = cursor.fetchone()
    
    if result:
        new_balance = result[0] + amount
        cursor.execute('UPDATE gamer_wallet SET balance = %s WHERE account_id = %s', (new_balance, gamer_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    else:
        cursor.close()
        conn.close()
        return False
