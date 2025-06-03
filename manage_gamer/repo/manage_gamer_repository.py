from shared.database import get_db_connection
from authentication.model.Role import Role
from authentication.model.AccountStatus import AccountStatus

def check_is_admin(admin_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM account WHERE id = %s", (admin_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result and result[0] == Role.ADMIN.name

def get_account_role(account_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM account WHERE id = %s", (account_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def ban_gamer_in_db(gamer_id, ban_reason):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE account SET status = %s WHERE id = %s", (AccountStatus.BANNED.name, gamer_id))
    cursor.execute("""
        INSERT INTO ban_detail (account_id, ban_reason, ban_date) 
        VALUES (%s, %s, NOW())
    """, (gamer_id, ban_reason))

    conn.commit()
    cursor.close()
    conn.close()

def unban_gamer_in_db(gamer_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Update status akun jadi NOT_BANNED
    cursor.execute(
        "UPDATE account SET status = %s WHERE id = %s",
        (AccountStatus.NOT_BANNED.name, gamer_id)
    )

    # Hapus data ban_detail untuk gamer yang diunban
    cursor.execute(
        "DELETE FROM ban_detail WHERE account_id = %s",
        (gamer_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

def search_gamers(username):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM account WHERE role = %s AND name LIKE %s"
    cursor.execute(query, (Role.GAMER.name, f"%{username}%"))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def search_banned_gamers(username):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT a.id, a.name, a.status, a.role, b.ban_reason
        FROM account a
        JOIN ban_detail b ON a.id = b.account_id
        WHERE a.role = %s AND a.status = %s AND a.name LIKE %s
    """
    cursor.execute(query, (Role.GAMER.name, AccountStatus.BANNED.name, f"%{username}%"))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_all_gamers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, status, role FROM account WHERE role = %s", (Role.GAMER.name,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    gamers = []
    for row in rows:
        gamers.append({
            'id': row[0],
            'name': row[1],
            'status': row[2],
            'role': row[3],
        })
    return gamers

def get_all_banned_gamers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.id, a.name, a.status, a.role, b.ban_reason, b.ban_date 
        FROM account a
        JOIN ban_detail b ON a.id = b.account_id
        WHERE a.role = %s AND a.status = %s
    """, (Role.GAMER.name, AccountStatus.BANNED.name))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    gamers = []
    for row in rows:
        gamers.append({
            'id': row[0],              # koma kurang di sini
            'name': row[1],
            'status': row[2],
            'role': row[3],
            'ban_reason': row[4],      # koma kurang juga
            'ban_date': row[5].strftime('%Y-%m-%d %H:%M:%S')
        })

    return gamers
