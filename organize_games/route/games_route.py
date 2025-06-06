from flask import Blueprint
from organize_games.controller import games_controller

publisher_bp = Blueprint(
    'publisher', 
    __name__,
    template_folder='../view',
    static_folder='../view',
    static_url_path='/publisher_static'
)

publisher_bp.route('/publisher_homepage/<int:publisher_id>')(games_controller.publisher_homepage_controller)


