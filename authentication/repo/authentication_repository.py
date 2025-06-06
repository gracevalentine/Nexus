from authentication.model.Role import Role
from authentication.model.AccountStatus import AccountStatus
from authentication.model.Gamer import Gamer
from authentication.model.Account import Account
from shared.database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

def get_account_by_email(email):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        SELECT id, name, email, password, role, status
        FROM account
        WHERE email = %s
    """, (email,))
    result = cursor.fetchone()
    db.close()

    if result:
        account_id, name, email, hashed_pw, role_str, status_str = result

        # Debug print untuk cek tipe sebelum konversi
        print(f'Debug: role_str={role_str} (type: {type(role_str)})')
        print(f'Debug: status_str={status_str} (type: {type(status_str)})')

        # Pastikan konversi dari string ke enum, pakai try-except supaya aman
        try:
            if isinstance(role_str, str):
                role = Role[role_str.upper()]  # pakai .upper() biar aman, misal 'gamer' jadi 'GAMER'
            else:
                role = role_str

            if isinstance(status_str, str):
                status = AccountStatus[status_str.upper()]
            else:
                status = status_str
        except KeyError as e:
            print(f'Error konversi role/status: {e}')
            return None

        # Debug print setelah konversi
        print(f'Debug: role={role} (type: {type(role)})')
        print(f'Debug: status={status} (type: {type(status)})')

        if role == Role.GAMER:
            wallet = get_gamer_wallet(account_id)
            return Gamer(name, email, hashed_pw, account_id, role=role, status=status, wallet=wallet)
        else:
            return Account(name, email, hashed_pw, account_id, role=role, status=status)

    return None

def get_gamer_wallet(account_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        SELECT balance FROM gamer_wallet WHERE account_id = %s
    """, (account_id,))
    result = cursor.fetchone()
    db.close()
    return result[0] if result else 0.0

def create_account(name, email, password, role: Role, status=AccountStatus.NOT_BANNED):
    hashed_pw = generate_password_hash(password)
    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("SELECT id FROM account WHERE email = %s", (email,))
        if cursor.fetchone():
            return {'success': False, 'error': 'Email sudah terdaftar'}

        cursor.execute("""
            INSERT INTO account (name, email, password, role, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, hashed_pw, role.name, status.name))
        account_id = cursor.lastrowid

        if role == Role.GAMER:
            cursor.execute("""
                INSERT INTO gamer_wallet (account_id, balance)
                VALUES (%s, %s)
            """, (account_id, 0.0))

        db.commit()
        return {'success': True, 'account_id': account_id}

    except Exception as e:
        db.rollback()
        return {'success': False, 'error': str(e)}

    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return check_password_hash(hashed_password, plain_password)