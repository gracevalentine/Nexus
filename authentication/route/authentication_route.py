from flask import Blueprint, redirect, render_template, session, url_for
from authentication.controller import authentication_controller

account_bp = Blueprint(
    'auth',  # penting! untuk url_for()
    __name__,
    template_folder='../view',
    static_folder='../view',
    static_url_path='/auth_static'
)

account_bp.route('/register', methods=['GET', 'POST'])(authentication_controller.register_controller)
account_bp.route('/login', methods=['GET', 'POST'])(authentication_controller.login_controller)
account_bp.route('/logout')(authentication_controller.logout_controller)

@account_bp.route('/gamer_homepage/<int:gamer_id>')
def gamer_homepage(gamer_id):
    if 'username' not in session:
        return redirect(url_for('auth.login_controller'))
    wallet = session.get('wallet', 0)
    username = session.get('username', 'Guest')
    return render_template('gamer_homepage.html', gamer_id=gamer_id, wallet_balance=wallet, username=username)