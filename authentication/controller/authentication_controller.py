from flask import request, redirect, url_for, render_template, session, flash
from authentication.repo import authentication_repository
from authentication.model.Role import Role
from authentication.model.AccountStatus import AccountStatus

def register_controller():
    if request.method == 'POST':
        name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        role_str = request.form.get('role', '').upper()

        if not all([name, email, password, confirm_password]):
            return render_template('signup.html', error='Semua field wajib diisi!')

        if password != confirm_password:
            return render_template('signup.html', error='Password dan konfirmasi tidak cocok.')

        try:
            role = Role[role_str]
        except KeyError:
            return render_template('signup.html', error='Role tidak valid')

        result = authentication_repository.create_account(name, email, password, role)
        if result['success']:
            flash('Akun berhasil dibuat! Silakan login.')
            return redirect(url_for('auth.login_controller'))
        else:
            return render_template('signup.html', error=result['error'])

    return render_template('signup.html')

def login_controller():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        data = authentication_repository.get_account_by_email(email)

        if not data:
            flash('Email tidak ditemukan.', 'error')
            return redirect(url_for('auth.login_controller'))

        account_id, name, email, hashed_pw, role_str, status_str = data
        role = Role[role_str]
        status = AccountStatus[status_str]

        if not authentication_repository.verify_password(password, hashed_pw):
            flash('Email atau password salah.', 'error')
            return redirect(url_for('auth.login_controller'))

        if status == AccountStatus.BANNED:
            return render_template('login.html', error='Akun anda telah diblokir.')

        # Set session
        session['account_id'] = account_id
        session['username'] = name
        session['role'] = role.name

        if role == Role.GAMER:
            wallet = authentication_repository.get_gamer_wallet(account_id)
            session['wallet'] = float(wallet)
            session['gamer_id'] = account_id
            flash('Berhasil login sebagai gamer!', 'success')
            return redirect(url_for('auth.gamer_homepage', gamer_id=account_id))

        elif role == Role.ADMIN:
            session['admin_id'] = account_id
            flash('Berhasil login sebagai admin!', 'success')
            return redirect(url_for('auth.admin_homepage', admin_id=account_id))

        elif role == Role.PUBLISHER:
            session['publisher_id'] = account_id
            flash('Berhasil login sebagai publisher!', 'success')
            return render_template('publisher/publisher_homepage.html', username=name, role=role.name)

        else:
            flash('Role tidak dikenali.', 'error')
            return redirect(url_for('auth.login_controller'))

    # GET method
    return render_template('login.html', error=None)

def logout_controller():
    session.clear()
    return redirect(url_for('auth.login_controller'))