from flask import Flask, redirect, url_for, send_from_directory
from controller.gamer_controller import gamer_bp
from controller.publisher_controller import publisher_bp 
from controller.admin_controller import admin_bp
from controller import account_controller
import os

app = Flask(__name__, template_folder='view', static_url_path='/css', static_folder='view/css')
app.register_blueprint(gamer_bp)
app.register_blueprint(publisher_bp) 
app.register_blueprint(admin_bp)
app.secret_key = 'secretkey123'

@app.route('/css/<path:filename>')
def custom_css(filename):
    return send_from_directory(os.path.join('view', 'css'), filename)

@app.route('/view/<path:filename>')
def custom_view_static(filename):
    return send_from_directory('view', filename)

@app.route('/view/asset/<path:filename>')
def bacground_admin(filename):
    return send_from_directory('view/asset', filename)

@app.route('/')
def index():
    return redirect(url_for('login_route'))

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    return account_controller.show_login()

@app.route('/register', methods=['GET', 'POST'])
def register_route():
    return account_controller.show_register()

# print(app.url_map)
app.add_url_rule('/logout', 'logout', account_controller.logout)

if __name__ == '__main__':
    app.run(debug=True)



