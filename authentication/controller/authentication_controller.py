from flask import request, redirect, url_for, render_template, session, flash
from authentication.repo import authentication_repository
from authentication.model.Role import Role
from authentication.model.AccountStatus import AccountStatus

# ----------- REGISTER -----------
def register_controller():
    if request.method == 'POST':
        name = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm-password', '').strip()
        role_str = request.form.get('role', '').upper()

        # Validasi field kosong
        if not all([name, email, password, confirm_password, role_str]):
            return render_template('signup.html', error='Semua field wajib diisi!')

        # Validasi password cocok
        if password != confirm_password:
            return render_template('signup.html', error='Password dan konfirmasi tidak cocok.')

        # Validasi role dari string ke enum
        try:
            role = Role[role_str]
        except KeyError:
            return render_template('signup.html', error='Role tidak valid.')

        # Buat akun
        result = authentication_repository.create_account(name, email, password, role)

        if result['success']:
            flash('Akun berhasil dibuat! Silakan login.', 'success')
            return redirect(url_for('auth.login_controller'))
        else:
            return render_template('signup.html', error=result.get('error', 'Terjadi kesalahan.'))

    return render_template('signup.html')


# ----------- LOGIN -----------
def login_controller():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            flash('Email dan password harus diisi.', 'error')
            return redirect(url_for('auth.login_controller'))

        account = authentication_repository.get_account_by_email(email)
        if account and authentication_repository.verify_password(password, account.password):
            if account.status == AccountStatus.BANNED:
                return render_template('login.html', error='Akun Anda telah diblokir.')

            # Set session
            session['account_id'] = account.id
            session['username'] = account.name
            session['role'] = account.role.name

            # Role khusus
            if account.role == Role.GAMER:
                session['wallet'] = getattr(account, 'wallet', 0.0)
                session['gamer_id'] = account.id
                flash('Berhasil login sebagai gamer!', 'success')
                return redirect(url_for('auth.gamer_homepage', gamer_id=account.id))

            elif account.role == Role.ADMIN:
                session['admin_id'] = account.id
                flash('Berhasil login sebagai admin!', 'success')
                return redirect(url_for('auth.admin_homepage', admin_id=account.id))

            elif account.role == Role.PUBLISHER:
                session['publisher_id'] = account.id
                flash('Berhasil login sebagai publisher!', 'success')
                return redirect(url_for('auth.publisher_homepage', publisher_id=account.id))

        flash('Email tidak ditemukan atau password salah.', 'error')
        return redirect(url_for('auth.login_controller'))

    return render_template('login.html', error=None)

# ----------- GAMER HOMEPAGE -----------
def gamer_homepage(gamer_id):
    if 'username' not in session or session.get('role') != 'GAMER':
        flash('Harap login terlebih dahulu.', 'error')
        return redirect(url_for('auth.login_controller'))

    wallet = session.get('wallet', 0)
    username = session.get('username', 'Guest')
    return render_template('gamer_homepage.html', gamer_id=gamer_id, wallet_balance=wallet, username=username)

# ----------- ADMIN HOMEPAGE -----------
def admin_homepage(admin_id):
    if 'username' not in session or session.get('role') != 'ADMIN':
        flash('Harap login terlebih dahulu.', 'error')
        return redirect(url_for('auth.login_controller'))

    return render_template('admin_homepage.html', admin_id=admin_id, username=session.get('username', 'Admin'))

# ----------- PUBLISHER HOMEPAGE -----------
def publisher_homepage(publisher_id):
    if 'username' not in session or session.get('role') != 'PUBLISHER':
        flash('Harap login terlebih dahulu.', 'error')
        return redirect(url_for('auth.login_controller'))

    return render_template('publisher_homepage.html', publisher_id=publisher_id, username=session.get('username', 'Publisher'))

# ----------- LOGOUT -----------
def logout_controller():
    session.clear()
    flash('Anda telah logout.', 'success')
    return redirect(url_for('auth.login_controller'))