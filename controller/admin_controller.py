from flask import Blueprint, abort, render_template, request, redirect, url_for
from model.Admin import Admin
from model.Account import Account
from model.AccountStatus import AccountStatus
from model.Role import Role
from model.Gamer import Gamer
from controller.db_controller import get_db_connection
from flask import redirect, url_for

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/ban/<int:gamer_id>')
def ban_gamer(gamer_id):
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

    cursor.execute("UPDATE account SET status = %s WHERE id = %s", (AccountStatus.BANNED.name, gamer_id))
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

    return redirect(url_for('admin.admin_view_unbanned_gamer_controller', admin_id=admin_id))

@admin_bp.route('/search_user', methods=['GET'])
def search_user():
    admin_id = request.args.get('admin_id')
    username = request.args.get('username')

    if not admin_id:
        abort(400, description="admin_id is required")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Cek apakah admin_id valid dan beneran admin
    cursor.execute("SELECT role FROM account WHERE id = %s", (admin_id,))
    result = cursor.fetchone()
    if not result or result[0] != Role.ADMIN.name:
        cursor.close()
        conn.close()
        abort(403, description="Access forbidden. You must be an admin.")

    # Lanjut query pencarian gamer
    query = "SELECT * FROM account WHERE role = %s AND name LIKE %s"
    cursor.execute(query, (Role.GAMER.name, f"%{username}%"))
    gamers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_view_gamer.html', admin_id=admin_id, gamers=gamers)

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

@admin_bp.route('/View Unbanned Gamer/<int:admin_id>')
def admin_view_unbanned_gamer_controller(admin_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, status, role FROM account WHERE role = %s AND status = %s", 
                   (Role.GAMER.name, AccountStatus.BANNED.name))
    rows = cursor.fetchall()

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

    return render_template('admin_unbanned_gamer.html', admin_id=admin_id, gamers=gamers)
