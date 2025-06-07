from flask import Blueprint, redirect, render_template, session, url_for
from store.controller import store_controller


store_bp = Blueprint(
    'gamer',
    __name__,
    template_folder='../view',
    static_folder='../view',
    static_url_path='/store_static'
)

store_bp.route('/store/<int:gamer_id>')(store_controller.storepage)
store_bp.route('/genre/<string:genre>/<int:gamer_id>')(store_controller.genre_detail)
store_bp.route('/review/list/<int:game_id>')(store_controller.get_reviews)
store_bp.route('/review/add/<int:gamer_id>/<int:game_id>', methods=['POST'])(store_controller.add_review)