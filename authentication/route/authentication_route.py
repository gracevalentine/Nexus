from flask import Blueprint
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