from flask import Blueprint, redirect, render_template, session, url_for
from authentication.controller import authentication_controller

account_bp = Blueprint(
    'auth', 
    __name__,
    template_folder='../view',
    static_folder='../view',
    static_url_path='/auth_static'
)

account_bp.route('/register', methods=['GET', 'POST'])(authentication_controller.register_controller)
account_bp.route('/login', methods=['GET', 'POST'])(authentication_controller.login_controller)
account_bp.route('/logout')(authentication_controller.logout_controller)
account_bp.route('/gamer_homepage/<int:gamer_id>')(authentication_controller.gamer_homepage)
account_bp.route('/admin_homepage/<int:admin_id>')(authentication_controller.admin_homepage)