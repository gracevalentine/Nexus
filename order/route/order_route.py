from flask import Blueprint, request, flash, redirect, url_for
from order.controller.order_controller import GamerController

gamer_bp = Blueprint(
    'ahhaa',
    __name__,
    template_folder='../view/html',   # path relatif dari order/route ke template
    static_folder='../view/css',      # path relatif ke folder CSS
    static_url_path='/gamer_static'   # URL prefix untuk akses CSS
)

@gamer_bp.route('/library/<int:gamer_id>')
def gamer_library(gamer_id):
    return GamerController.library(gamer_id)

# @gamer_bp.route('/storepage/<int:gamer_id>')
# def gamer_storepage(gamer_id):
#     return GamerController.storepage(gamer_id)

# @gamer_bp.route('/storepage/genre/<genre>/<int:gamer_id>')
# def genre_detail(genre, gamer_id):
#     return GamerController.genre_detail(genre, gamer_id)

# @gamer_bp.route('/buy/<int:gamer_id>/<int:game_id>', methods=['POST'])
# def buy_game(gamer_id, game_id):
#     return GamerController.buy_game(gamer_id, game_id)

# @gamer_bp.route('/uninstall/<int:gamer_id>/<int:game_id>', methods=['POST'])
# def uninstall_game(gamer_id, game_id):
#     return GamerController.uninstall_game(gamer_id, game_id)

# @gamer_bp.route('/cart/<int:gamer_id>')
# def show_cart(gamer_id):
#     return GamerController.show_cart(gamer_id)

# @gamer_bp.route('/cart/add/<int:gamer_id>/<int:game_id>', methods=['POST'])
# def add_to_cart(gamer_id, game_id):
#     return GamerController.add_to_cart(gamer_id, game_id)

# @gamer_bp.route('/cart/remove/<int:gamer_id>/<int:game_id>', methods=['POST'])
# def remove_from_cart(gamer_id, game_id):
#     GamerController.remove_from_cart(gamer_id, game_id)
#     return redirect(url_for('gamer.show_cart', gamer_id=gamer_id))

# @gamer_bp.route('/cart/checkout/<int:gamer_id>', methods=['POST'])
# def checkout(gamer_id):
#     selected_game_ids = request.form.getlist('selected_games')
#     selected_game_ids = list(map(int, selected_game_ids))
#     return GamerController.checkout(gamer_id, selected_game_ids)

# @gamer_bp.route('/review/<int:gamer_id>/<int:game_id>', methods=['POST'])
# def add_review(gamer_id, game_id):
#     data = request.get_json()
#     review_text = data.get('review')
#     return GamerController.add_review(gamer_id, game_id, review_text)

# @gamer_bp.route('/gamer/review/list/<int:game_id>')
# def get_reviews(game_id):
#     return GamerController.get_reviews(game_id)
