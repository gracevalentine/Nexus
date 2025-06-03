from flask import Flask, redirect, render_template, url_for
from authentication.route.authentication_route import account_bp
from manage_gamer.route.manage_gamer_route import admin_bp

from flask import Flask
from order.route.order_route import gamer_bp  # import blueprint gamer
from jinja2 import ChoiceLoader, FileSystemLoader

app = Flask(__name__)


app.jinja_loader = ChoiceLoader([
    FileSystemLoader('view'),
    FileSystemLoader('manage_gamer/view'),
    FileSystemLoader('order/view/html'),
    FileSystemLoader('authentication/view/html')
])

app.secret_key = 'secretkey123'

app.register_blueprint(account_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(gamer_bp, url_prefix='/gamer')

@app.route('/')
def home():
    return redirect(url_for('auth.login_controller'))

@app.route('/gamer-list')
def gamer_list():
    return render_template('admin_view_gamer.html')

if __name__ == '__main__':
    app.run(debug=True)
