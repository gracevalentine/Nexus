from flask import Blueprint, render_template, request, redirect, url_for
from model.Admin import Admin
from model.Account import Account
from model.Transaction import Transaction
from model.AccountStatus import AccountStatus
from model.Role import Role
from model.Gamer import Gamer

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# controller/admin.py
from model.Gamer import Gamer
from model.AccountStatus import AccountStatus
from flask import redirect, url_for


@admin_bp.route('/ban/<int:gamer_id>')
def ban_gamer(gamer_id):
    # Gunakan query ORM untuk ambil data gamer dari DB
    gamer = Gamer.query.get(gamer_id)  # Query ORM, bukan OOP biasa
    if gamer:
        gamer.set_status(AccountStatus.BANNED)  # Mengupdate status di objek
        db.session.commit()  # Simpan perubahan ke DB
    return redirect(url_for('admin.view_gamers'))
