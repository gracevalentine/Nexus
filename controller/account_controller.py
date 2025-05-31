from flask import request, redirect, url_for, render_template, session, flash
from model.Account import Role
from model.AccountStatus import AccountStatus
from controller.db_controller import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

def show_register():
    if request.method == 'POST':
        name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        role_str = request.form.get('role').upper()

        try:
            role = Role[role_str]
        except KeyError:
            return render_template('signUp.html', error='Role tidak valid')

        status = AccountStatus.NOT_BANNED

        if not all([name, email, password, confirm_password]):
            return render_template('signUp.html', error='Semua field wajib diisi!')

        if password != confirm_password:
            return render_template('signUp.html', error='Password dan konfirmasi tidak cocok.')

        hashed_pw = generate_password_hash(password)

        try:
            db = get_db_connection()
            cursor = db.cursor()

            # Cek apakah email sudah terdaftar
            cursor.execute("SELECT id FROM account WHERE email = %s", (email,))
            existing = cursor.fetchone()
            if existing:
                return render_template('signUp.html', error='Email sudah terdaftar.')

            # Insert ke tabel account
            cursor.execute("""
                INSERT INTO account (name, email, password, role, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, hashed_pw, role.name, status.name))

            account_id = cursor.lastrowid

            # Insert ke gamer_data kalau role GAMER
            if role == Role.GAMER:
                cursor.execute("""
                    INSERT INTO gamer_wallet (account_id, balance)
                    VALUES (%s, %s)
                """, (account_id, 0.0))
                print("🎮 gamer_data ditambahkan")

            db.commit()

            # ✅ Notifikasi berhasil signup
            flash('Akun berhasil dibuat! Silakan login.')
            return redirect(url_for('login_route'))

        except Exception as e:
            db.rollback()
            return render_template('signUp.html', error=f"Gagal daftar: {str(e)}")

        finally:
            db.close()

    return render_template('signUp.html')

def show_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor()

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

                wallet = None
                if role == Role.GAMER:
                    cursor.execute("""
                        SELECT balance FROM gamer_wallet WHERE account_id = %s
                    """, (account_id,))
                    gamer_row = cursor.fetchone()
                    wallet = gamer_row[0] if gamer_row else 0.0

                db.close()

                session['account_id'] = account_id
                session['username'] = name
                session['role'] = role.name
                if wallet is not None:
                    session['wallet'] = float(wallet)

                # ✅ Flash sukses login
                flash('Berhasil login!')

                if role == Role.GAMER:
                    return redirect(url_for('gamer.gamer_homepage', gamer_id=account_id))
                elif role == Role.ADMIN:
                    return redirect(url_for('admin.admin_view_gamer_controller', admin_id=account_id))
                elif role == Role.PUBLISHER:
                    return redirect(url_for('publisher.publisher_homepage', publisher_id=account_id))

            else:
                db.close()
                # ❌ Login gagal → redirect ke signup
                flash('Email atau password salah. Daftar akun baru.')
                return redirect(url_for('register_route'))

        db.close()
        # ❌ Email tidak ditemukan → redirect ke signup
        flash('Email tidak ditemukan. Silakan daftar terlebih dahulu.')
        return redirect(url_for('register_route'))

    return render_template('login.html')


def home():
    if 'account_id' not in session:
        return redirect(url_for('login_route'))
    
    return render_template('home_page.html', username=session.get('username'), role=session.get('role'))


def dashboard_route():
    return f"Welcome {session.get('username')} as {session.get('role')}"


def logout():
    session.clear()
    return redirect(url_for('login_route'))
