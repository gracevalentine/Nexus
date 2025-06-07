from flask import Flask, redirect, render_template, url_for
from authentication.route.authentication_route import account_bp
from manage_gamer.route.manage_gamer_route import admin_bp
from store.route.store_route import store_bp  
from order.route.order_route import order_bp
from wallet.route.wallet_route import wallet_bp
from organize_game.route.organize_game_route import publisher_bp
from jinja2 import ChoiceLoader, FileSystemLoader

app = Flask(__name__)

app.jinja_loader = ChoiceLoader([
    FileSystemLoader('view'),
    FileSystemLoader('manage_gamer/view'),
    FileSystemLoader('order/view'),
    FileSystemLoader('store/view'),
    FileSystemLoader('wallet/view'),
    FileSystemLoader('organize_game/view')
])

app.secret_key = 'secretkey123'

app.register_blueprint(account_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(store_bp, url_prefix='/gamer')
app.register_blueprint(order_bp, url_prefix='/order')
app.register_blueprint(wallet_bp, url_prefix='/gamer')
app.register_blueprint(publisher_bp, url_prefix='/publisher')

@app.route('/')
def home():
    return redirect(url_for('auth.login_controller'))

if __name__ == '__main__':
    app.run(debug=True)
