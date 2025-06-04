from flask import Blueprint, redirect, render_template, session, url_for
from manage_gamer.controller import manage_gamer_controller

admin_bp = Blueprint(
    'admin', 
    __name__,
    template_folder='../view',
    static_folder='../view',
    static_url_path='/admin_static'
)

admin_bp.route('/ban/<int:gamer_id>', methods=['POST'])(manage_gamer_controller.ban_gamer_controller)
admin_bp.route('/unban/<int:gamer_id>', methods=['GET', 'POST'])(manage_gamer_controller.unban_gamer_controller)
admin_bp.route('/searchUser')(manage_gamer_controller.search_user_controller)
admin_bp.route('/searchBannedUser')(manage_gamer_controller.search_banned_user_controller)
admin_bp.route('/viewGamer')(manage_gamer_controller.admin_view_gamer_controller)
admin_bp.route('/viewBannedGamer')(manage_gamer_controller.admin_view_banned_gamer_controller)
admin_bp.route('/admin_homepage/<int:admin_id>')(manage_gamer_controller.admin_homepage_controller)


