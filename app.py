# from flask import Flask, render_template, request, redirect, url_for
# from controller import account_controller

# app = Flask(__name__, template_folder='view', static_folder='view')
# app.secret_key = 'some_random_secret_key'

# @app.route('/')
# def home():
#     return render_template('login.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login_route():  # ⬅️ ganti jadi login_route biar sesuai dengan controller
#     return account_controller.show_login()

# @app.route('/register', methods=['GET', 'POST'])
# def register_route():  # ⬅️ ini route baru untuk register
#     return account_controller.show_register()

# # @app.route('/gamer/<int:user_id>')
# # def gamer_dashboard(user_id):
# #     return f"Welcome Gamer #{user_id}!"

# @app.route('/gamer/<int:user_id>')
# def gamer_dashboard(user_id):
#     return render_template('home_page.html', user_id=user_id)

# @app.route('/admin/<int:admin_id>')
# def admin_dashboard(admin_id):
#     return f"Welcome Admin #{admin_id}!"

# @app.route('/publisher/<int:publisher_id>')
# def publisher_dashboard(publisher_id):
#     return f"Welcome Publisher #{publisher_id}!"

# if __name__ == '__main__':
#     app.run(debug=True)

# dari yang dea
from flask import Flask, redirect, url_for, send_from_directory
from controller import account_controller
import os

app = Flask(__name__, template_folder='view', static_url_path='/css', static_folder='view/css')
app.secret_key = 'secretkey123'

# Tambahan: untuk layani CSS dari view/css
@app.route('/css/<path:filename>')
def custom_css(filename):
    return send_from_directory(os.path.join('view', 'css'), filename)

@app.route('/')
def index():
    return redirect(url_for('login_route'))

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    return account_controller.show_login()

@app.route('/register', methods=['GET', 'POST'])
def register_route():
    return account_controller.show_register()

if __name__ == '__main__':
    app.run(debug=True)



