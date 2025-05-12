from flask import Flask, render_template, request, redirect, url_for
from controller import account_controller

app = Flask(__name__, template_folder='view', static_folder='view')
app.secret_key = 'some_random_secret_key'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login_route():  # ⬅️ ganti jadi login_route biar sesuai dengan controller
    return account_controller.show_login()

@app.route('/register', methods=['GET', 'POST'])
def register_route():  # ⬅️ ini route baru untuk register
    return account_controller.show_register()

# @app.route('/gamer/<int:user_id>')
# def gamer_dashboard(user_id):
#     return f"Welcome Gamer #{user_id}!"

@app.route('/gamer/<int:user_id>')
def gamer_dashboard(user_id):
    return render_template('home_page.html', user_id=user_id)

@app.route('/admin/<int:admin_id>')
def admin_dashboard(admin_id):
    return f"Welcome Admin #{admin_id}!"

@app.route('/publisher/<int:publisher_id>')
def publisher_dashboard(publisher_id):
    return f"Welcome Publisher #{publisher_id}!"

if __name__ == '__main__':
    app.run(debug=True)
