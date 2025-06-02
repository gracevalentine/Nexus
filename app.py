from flask import Flask, redirect, url_for
from authentication.route.authentication_route import account_bp

app = Flask(__name__)
app.secret_key = 'secretkey123'

app.register_blueprint(account_bp, url_prefix='/auth')

@app.route('/')
def home():
    return redirect(url_for('auth.login_controller'))

if __name__ == '__main__':
    app.run(debug=True)
