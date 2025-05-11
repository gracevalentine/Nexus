from flask import Flask, render_template, request, redirect, url_for
from controller import account_controller
from model.AccountStatus import AccountStatus

app = Flask(__name__, template_folder='view')

@app.route('/')
def home():
    return render_template('home_page.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']

        account = account_controller.get_account(username, password)

        if account and account.status == AccountStatus.ACTIVE:
            if account.role.name == "GAMER":
                return redirect(url_for('gamer_dashboard', user_id=account.id))
            elif account.role.name == "ADMIN":
                return redirect(url_for('admin_dashboard', admin_id=account.id))
            elif account.role.name == "PUBLISHER":
                return redirect(url_for('publisher_dashboard', publisher_id=account.id))
        else:
            error = "Invalid username or password"

    return render_template('login.html', error=error)

@app.route('/gamer/<int:user_id>')
def gamer_dashboard(user_id):
    return f"Welcome Gamer #{user_id}!"

@app.route('/admin/<int:admin_id>')
def admin_dashboard(admin_id):
    return f"Welcome Admin #{admin_id}!"

@app.route('/publisher/<int:publisher_id>')
def publisher_dashboard(publisher_id):
    return f"Welcome Publisher #{publisher_id}!"

if __name__ == '__main__':
    app.run(debug=True)
