from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from manage_gamer.repo import manage_gamer_repository  # pastikan path sesuai
from authentication.model.AccountStatus import AccountStatus

admin_bp = Blueprint('admin', __name__)

# Halaman semua gamer
@admin_bp.route('/viewGamer')
def admin_view_gamer_controller():
    admin_id = session.get('admin_id')
    if not admin_id or not manage_gamer_repository.check_is_admin(admin_id):
        print(f"[LOG] admin_id from session: {admin_id}")
        abort(403)

    gamers = manage_gamer_repository.get_all_gamers()
    return render_template('admin_view_gamer.html', admin_id=admin_id, gamers=gamers)

# Halaman gamer yang di-banned
@admin_bp.route('/viewBannedGamer')
def admin_view_banned_gamer_controller():
    admin_id = session.get('admin_id')
    if not admin_id or not manage_gamer_repository.check_is_admin(admin_id):
        abort(403)

    gamers = manage_gamer_repository.get_all_banned_gamers()
    return render_template('admin_view_banned_gamer.html', admin_id=admin_id, gamers=gamers)

# Ban gamer
@admin_bp.route('/ban/<int:gamer_id>', methods=['POST'])
def ban_gamer_controller(gamer_id):
    admin_id = session.get('admin_id')
    ban_reason = request.form.get('ban_reason')

    if not admin_id or not manage_gamer_repository.check_is_admin(admin_id):
        abort(403)

    VALID_BAN_REASONS = {'SPAM', 'CHEATING', 'ABUSE', 'OTHER'}
    if ban_reason not in VALID_BAN_REASONS:
        abort(400, description="Invalid ban reason")

    manage_gamer_repository.ban_gamer_in_db(gamer_id, ban_reason)
    return redirect(url_for('admin.admin_view_gamer_controller'))

# Unban gamer
@admin_bp.route('/unban/<int:gamer_id>', methods=['POST'])
def unban_gamer_controller(gamer_id):
    admin_id = session.get('admin_id')
    if not admin_id or not manage_gamer_repository.check_is_admin(admin_id):
        abort(403)

    manage_gamer_repository.unban_gamer_in_db(gamer_id)
    return redirect(url_for('admin.admin_view_banned_gamer_controller'))

# Search gamer aktif
@admin_bp.route('/searchUser')
def search_user_controller():
    admin_id = session.get('admin_id')
    username = request.args.get('username', '')

    if not admin_id or not manage_gamer_repository.check_is_admin(admin_id):
        abort(403)

    gamers = manage_gamer_repository.search_gamers(username)
    return render_template('admin_view_gamer.html', admin_id=admin_id, gamers=gamers)

# Search gamer yang di-banned
@admin_bp.route('/searchBannedUser')
def search_banned_user_controller():
    admin_id = session.get('admin_id')
    username = request.args.get('username', '')

    if not admin_id or not manage_gamer_repository.check_is_admin(admin_id):
        abort(403)

    gamers = manage_gamer_repository.search_banned_gamers(username)
    return render_template('admin_view_banned_gamer.html', admin_id=admin_id, gamers=gamers)
