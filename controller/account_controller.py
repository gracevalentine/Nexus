from flask import request, redirect, url_for, render_template, session
from model.Account import Account, Role
from model.AccountStatus import AccountStatus
from controller.db_controller import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

def show_register():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        role = Role[request.form['role'].upper()]
        status = AccountStatus.ACTIVE

        if password != confirm_password:
            return render_template('signUp.html', error='Passwords do not match')

        # Hash the password using bcrypt (instead of MD5)
        hashed_pw = generate_password_hash(password)  # bcrypt hashing

        try:
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO accounts (name, email, password, role, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, hashed_pw, role.name, status.name))
            db.commit()
            db.close()
            
            # If successful, redirect to login page
            return redirect(url_for('login_route'))
        except Exception as e:
            db.rollback()  # In case of error, rollback the transaction
            return render_template('signUp.html', error=f"Error: {str(e)}")
    
    return render_template('signUp.html')

def show_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT id, name, password, role, status FROM accounts WHERE email=%s", (email,))
        data = cursor.fetchone()
        db.close()

        if data:
            # Debugging: Print the hashed password from the DB
            print("Stored hashed password:", data[2])
            print("Password entered:", password)

            # Verify password using bcrypt
            if check_password_hash(data[2], password):  # Check against hashed password
                account = Account(
                    name=data[1],
                    email=email,
                    password=data[2],  # hashed password (nggak perlu disimpan kalau ga dipakai)
                    id=data[0],
                    role=Role[data[3]],
                    status=AccountStatus[data[4]]
                )

                if account.status == AccountStatus.BANNED:
                    return render_template('login.html', error='Akun anda telah diblokir')

                session['account_id'] = account.id
                session['username'] = account.name
                session['role'] = account.role.name

                # Redirect berdasar role
                if account.role == Role.GAMER:
                    return redirect(url_for('gamer_dashboard', user_id=account.id))
                elif account.role == Role.ADMIN:
                    return redirect(url_for('admin_dashboard', admin_id=account.id))
                elif account.role == Role.PUBLISHER:
                    return redirect(url_for('publisher_dashboard', publisher_id=account.id))
            else:
                return render_template('login.html', error='Email atau password salah')

        else:
            return render_template('login.html', error='Email tidak ditemukan')

    return render_template('login.html')

def home():
    if 'account_id' not in session:
        return redirect(url_for('login_route'))
    
    return render_template('home.html', username=session.get('username'), role=session.get('role'))

def dashboard_route():
    return f"Welcome {session.get('username')} as {session.get('role')}"

def logout():
    session.clear()
    return redirect(url_for('login_route'))
