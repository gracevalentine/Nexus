from flask import Flask, redirect, render_template, url_for
from authentication.route.authentication_route import account_bp
from manage_gamer.route.manage_gamer_route import admin_bp
from store.route.store_route import store_bp  
from organize_games.route.games_route import publisher_bp
from jinja2 import ChoiceLoader, FileSystemLoader

app = Flask(__name__)

app.jinja_loader = ChoiceLoader([
    FileSystemLoader('view'),
    FileSystemLoader('manage_gamer/view'),
    FileSystemLoader('order/view'),
    FileSystemLoader('store/view'),
    FileSystemLoader('organize_gamer/view')
])

app.secret_key = 'secretkey123'

app.register_blueprint(account_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(store_bp, url_prefix='/gamer')
app.register_blueprint(publisher_bp, url_prefix='/publisher')

@app.route('/')
def home():
    return redirect(url_for('auth.login_controller'))

if __name__ == '__main__':
    app.run(debug=True)
