from flask import Blueprint
from order.controller import order_controller 

order_bp = Blueprint(
    'order',
    __name__,
    template_folder='../view',   # path relatif dari order/route ke template
    static_folder='../view',      # path relatif ke folder CSS
    static_url_path='/order_static'   # URL prefix untuk akses CSS
)

order_bp.route('/library/<int:gamer_id>')(order_controller.library)
order_bp.route('/cart/<int:gamer_id>')(order_controller.show_cart)
order_bp.route('/cart/checkout/<int:gamer_id>', methods=['POST'])(order_controller.checkout)
order_bp.route('/cart/add/<int:gamer_id>/<int:game_id>', methods=['POST'])(order_controller.add_to_cart)
order_bp.route('/cart/remove/<int:gamer_id>/<int:game_id>', methods=['POST'])(order_controller.remove_from_cart)
order_bp.route('/buy/<int:gamer_id>/<int:game_id>', methods=['POST'])(order_controller.buy_game)
order_bp.route('/uninstall/<int:gamer_id>/<int:game_id>', methods=['POST'])(order_controller.uninstall_game)
order_bp.route('/review/list/<int:game_id>')(order_controller.get_reviews)
order_bp.route('/review/add/<int:gamer_id>/<int:game_id>', methods=['POST'])(order_controller.add_review)

# def remove_from_cart(gamer_id, game_id):
#     GamerController.remove_from_cart(gamer_id, game_id)
#     return redirect(url_for('gamer.show_cart', gamer_id=gamer_id))
# def add_to_cart(gamer_id, game_id):
#     return GamerController.add_to_cart(gamer_id, game_id)

# @gamer_bp.route('/storepage/<int:gamer_id>')
# def gamer_storepage(gamer_id):
#     return GamerController.storepage(gamer_id)

# @gamer_bp.route('/storepage/genre/<genre>/<int:gamer_id>')
# def genre_detail(genre, gamer_id):
#     return GamerController.genre_detail(genre, gamer_id)





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

