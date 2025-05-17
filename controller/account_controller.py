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
        status = AccountStatus.NOT_BANNED

        if password != confirm_password:
            return render_template('signUp.html', error='Passwords do not match')

        hashed_pw = generate_password_hash(password)

        try:
            db = get_db_connection()
            cursor = db.cursor()

            # Masukkan ke tabel account
            cursor.execute("""
                INSERT INTO account (name, email, password, role, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, hashed_pw, role.name, status.name))

            account_id = cursor.lastrowid

            # Jika role-nya GAMER, tambahkan ke tabel gamer_data
            if role == Role.GAMER:
                cursor.execute("""
                    INSERT INTO gamer_data (account_id, wallet)
                    VALUES (%s, %s)
                """, (account_id, 0.0))

            db.commit()
            return redirect(url_for('login_route'))

        except Exception as e:
            db.rollback()
            return render_template('signUp.html', error=f"Error: {str(e)}")

        finally:
            db.close()

    return render_template('signUp.html')

def show_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor()

        # Ambil data dari tabel account
        cursor.execute("""
            SELECT id, name, email, password, role, status
            FROM account
            WHERE email = %s
        """, (email,))
        data = cursor.fetchone()

        if data:
            account_id, name, email, hashed_pw, role_str, status_str = data
            role = Role[role_str]
            status = AccountStatus[status_str]

            if check_password_hash(hashed_pw, password):
                if status == AccountStatus.BANNED:
                    return render_template('login.html', error='Akun anda telah diblokir')

                # Optional: ambil data tambahan kalau role-nya GAMER
                wallet = None
                if role == Role.GAMER:
                    cursor.execute("""
                        SELECT wallet FROM gamer_data WHERE account_id = %s
                    """, (account_id,))
                    gamer_row = cursor.fetchone()
                    wallet = gamer_row[0] if gamer_row else 0.0

                db.close()

                # Simpan session
                session['account_id'] = account_id
                session['username'] = name
                session['role'] = role.name
                if wallet is not None:
                    session['wallet'] = float(wallet)

                # Redirect sesuai role
                if role == Role.GAMER:
                    return redirect(url_for('gamer.gamer_homepage', gamer_id=account_id))
                elif role == Role.ADMIN:
                    return redirect(url_for('admin_dashboard', admin_id=account_id))
                elif role == Role.PUBLISHER:
                    return redirect(url_for('publisher.publisher_homepage', publisher_id=account_id))

            else:
                db.close()
                return render_template('login.html', error='Email atau password salah')

        db.close()
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
