from flask import Blueprint, render_template, request, redirect, url_for
from model.Admin import Admin
from model.Account import Account
from model.Transaction import Transaction
from model.AccountStatus import AccountStatus
from model.Role import Role
from model.Gamer import Gamer

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# # Simulasi database sementara (bisa ganti nanti dengan db beneran)
# users = [
#     Account("Gamer1", "gamer1@email.com", "pass", 1, Role.GAMER, AccountStatus.ACTIVE),
#     Account("Gamer2", "gamer2@email.com", "pass", 2, Role.GAMER, AccountStatus.BANNED),
#     Account("Gamer3", "gamer3@email.com", "pass", 3, Role.GAMER, AccountStatus.ACTIVE),
# ]

# transactions = [
#     Transaction(1, 1),
#     Transaction(2, 3)
# ]

# # View semua transaksi
# @admin_bp.route('/transactions')
# def view_transactions():
#     return render_template('admin/transactions.html', transactions=transactions)

# # View semua gamer
# @admin_bp.route('/gamers')
# def view_gamers():
#     gamers = [user for user in users if user.get_role() == Role.GAMER]
#     return render_template('admin/gamers.html', gamers=gamers)

# # View gamer yang dibanned
# @admin_bp.route('/banned_gamers')
# def view_banned_gamers():
#     banned = [user for user in users if user.get_role() == Role.GAMER and user.get_status() == AccountStatus.BANNED]
#     return render_template('admin/banned_gamers.html', banned_gamers=banned)

@admin_bp.route('/ban/<int:gamer_id>')
def ban_gamer(gamer_id):
    for user in users:
        if isinstance(user, Gamer) and user.id == gamer_id:
            user.set_status(AccountStatus.BANNED)
            break
    return redirect(url_for('admin.view_gamers'))
