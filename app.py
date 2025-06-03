from flask import Flask, redirect, url_for
from authentication.route.authentication_route import account_bp
from order.route.order_route import gamer_bp  # import blueprint gamer
from jinja2 import ChoiceLoader, FileSystemLoader

app = Flask(__name__)

# Setup custom template loader biar bisa load template dari banyak folder sekaligus
app.jinja_loader = ChoiceLoader([
    FileSystemLoader('order/view/html'),
    FileSystemLoader('authentication/view/html'),
    # tambahin folder lain sesuai kebutuhan lo
])

app.secret_key = 'secretkey123'

app.register_blueprint(account_bp, url_prefix='/auth')
app.register_blueprint(gamer_bp, url_prefix='/gamer')

@app.route('/')
def home():
    return redirect(url_for('auth.login_controller'))

if __name__ == '__main__':
    app.run(debug=True)
