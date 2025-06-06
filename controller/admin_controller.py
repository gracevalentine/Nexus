from flask import Blueprint, abort, render_template, request, redirect, url_for
from model.Account import Account
from model.AccountStatus import AccountStatus
from model.Role import Role
from authentication.model.Gamer import Gamer
from controller.db_controller import get_db_connection
from flask import redirect, url_for

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/ban/<int:gamer_id>', methods=['POST'])
def ban_gamer(gamer_id):
    admin_id = request.form.get('admin_id')
    
    VALID_BAN_REASONS = {'SPAM', 'CHEATING', 'ABUSE', 'OTHER'}
    ban_reason = request.form.get('ban_reason')
    
    if not admin_id:
        abort(400, description="admin_id is required")
        
    if ban_reason not in VALID_BAN_REASONS:
        abort(400, description="Invalid ban reason")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT role FROM account WHERE id = %s", (admin_id,))
    result = cursor.fetchone()
    if not result or result[0] != Role.ADMIN.name:
        abort(403, description="Access forbidden. You must be an admin.")

    cursor.execute("SELECT role FROM account WHERE id = %s", (gamer_id,))
    gamer_result = cursor.fetchone()
    if not gamer_result:
        abort(404, description="Gamer not found")
    if gamer_result[0] != Role.GAMER.name:
        abort(400, description="Only gamers can be banned")

    # Update status akun jadi BANNED
    cursor.execute("UPDATE account SET status = %s WHERE id = %s", (AccountStatus.BANNED.name, gamer_id))

    # Insert detail banned ke tabel ban_detail
    query_insert_ban = """
    INSERT INTO ban_detail (account_id, ban_reason, ban_date) 
    VALUES (%s, %s, NOW())
    """
    cursor.execute(query_insert_ban, (gamer_id, ban_reason))

    
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin.admin_view_gamer_controller', admin_id=admin_id))

@admin_bp.route('/unbannedGamer/<int:gamer_id>')
def unban_gamer(gamer_id):
    admin_id = request.args.get('admin_id')
    if not admin_id:
        abort(400, description="admin_id is required")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT role FROM account WHERE id = %s", (admin_id,))
    result = cursor.fetchone()
    if not result or result[0] != Role.ADMIN.name:
        abort(403, description="Access forbidden. You must be an admin.")

    cursor.execute("SELECT role FROM account WHERE id = %s", (gamer_id,))
    gamer_result = cursor.fetchone()
    if not gamer_result:
        abort(404, description="Gamer not found")
    if gamer_result[0] != Role.GAMER.name:
        abort(400, description="Only gamers can be banned")

    cursor.execute("UPDATE account SET status = %s WHERE id = %s", (AccountStatus.NOT_BANNED.name, gamer_id))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin.admin_view_banned_gamer_controller', admin_id=admin_id))

@admin_bp.route('/search_user', methods=['GET'])
def search_user():
    admin_id = request.args.get('admin_id')
    username = request.args.get('username', '')  

    if not admin_id:
        abort(400, description="admin_id is required")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Cek apakah admin_id memang admin
    cursor.execute("SELECT role FROM account WHERE id = %s", (admin_id,))
    result = cursor.fetchone()
    if not result or result['role'] != Role.ADMIN.name:
        cursor.close()
        conn.close()
        abort(403, description="Access forbidden. You must be an admin.")

    # Query pencarian gamer dengan role GAMER dan nama mirip username
    query = "SELECT * FROM account WHERE role = %s AND name LIKE %s"
    cursor.execute(query, (Role.GAMER.name, f"%{username}%"))
    gamers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_view_gamer.html', admin_id=admin_id, gamers=gamers)

@admin_bp.route('/search_banned_user', methods=['GET'])
def search_banned_user():
    admin_id = request.args.get('admin_id')
    username = request.args.get('username', '')

    if not admin_id:
        abort(400, description="admin_id is required")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Cek admin
    cursor.execute("SELECT role FROM account WHERE id = %s", (admin_id,))
    result = cursor.fetchone()
    if not result or result['role'] != Role.ADMIN.name:
        cursor.close()
        conn.close()
        abort(403, description="Access forbidden. You must be an admin.")

    query = """
    SELECT a.id, a.name, a.status, a.role, b.ban_reason
    FROM account a
    JOIN ban_detail b ON a.id = b.account_id
    WHERE a.role = %s AND a.status = %s AND a.name LIKE %s
    """
    cursor.execute(query, (Role.GAMER.name, AccountStatus.BANNED.name, f"%{username}%"))
    gamers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_view_banned_gamer.html', admin_id=admin_id, gamers=gamers)

@admin_bp.route('/View Gamer/<int:admin_id>')
def admin_view_gamer_controller(admin_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Ambil kolom yang dipakai aja, biar urut
    cursor.execute("SELECT id, name, status, role FROM account WHERE role = %s", (Role.GAMER.name,))
    rows = cursor.fetchall()

    # Ubah dari list of tuple → list of dict
    gamers = []
    for row in rows:
        gamers.append({
            'id': row[0],
            'name': row[1],
            'status': row[2],
            'role': row[3],
        })

    cursor.close()
    conn.close()
    
    return render_template('admin_view_gamer.html', admin_id=admin_id, gamers=gamers)

@admin_bp.route('/View banned Gamer/<int:admin_id>')
def admin_view_banned_gamer_controller(admin_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query gabungan untuk ambil data banned gamer + alasan banned
    cursor.execute("""
        SELECT a.id, a.name, a.status, a.role, b.ban_reason 
        FROM account a
        JOIN ban_detail b ON a.id = b.account_id
        WHERE a.role = %s AND a.status = %s
    """, (Role.GAMER.name, AccountStatus.BANNED.name))

    rows = cursor.fetchall()

    gamers = []
    for row in rows:
        gamers.append({
            'id': row[0],
            'name': row[1],
            'status': row[2],
            'role': row[3],
            'ban_reason': row[4]
        })

    cursor.close()
    conn.close()

    return render_template('admin_view_banned_gamer.html', admin_id=admin_id, gamers=gamers)

