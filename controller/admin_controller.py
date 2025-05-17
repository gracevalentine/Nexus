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

    return redirect(url_for('admin.admin_homepage', admin_id=admin_id))

@admin_bp.route('/dashboard/<int:admin_id>')
def admin_homepage(admin_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM account WHERE role = %s", (Role.GAMER.name,))
    gamers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin_home_page.html', admin_id=admin_id, gamers=gamers)



