from flask import Blueprint
from organize_game.controller import organize_game_controller

publisher_bp = Blueprint(
    'publisher', 
    __name__,
    template_folder='../view',
    static_folder='../view',
    static_url_path='/publisher_static'
)

publisher_bp.route('/publisher_homepage/<int:publisher_id>')(organize_game_controller.publisher_homepage)
publisher_bp.route('/published_games/<int:publisher_id>')(organize_game_controller.published_games)
publisher_bp.route('/add_game/<int:publisher_id>', methods=['GET', 'POST'])(organize_game_controller.add_new_game)
publisher_bp.route('/edit_game/<int:publisher_id>/<int:game_id>', methods=['GET', 'POST'])(organize_game_controller.edit_game)
publisher_bp.route('/delete_game/<int:publisher_id>/<int:game_id>', methods=['POST'])(organize_game_controller.delete_game)