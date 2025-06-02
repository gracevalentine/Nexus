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

        if data:
            account_id, name, email, hashed_pw, role_str, status_str = data
            role = Role[role_str]
            status = AccountStatus[status_str]

            if not authentication_repository.verify_password(password, hashed_pw):
                flash('Email atau password salah.')
                return redirect(url_for('auth.login_controller'))

            if status == AccountStatus.BANNED:
                return render_template('login.html', error='Akun anda telah diblokir.')

            session['account_id'] = account_id
            session['username'] = name
            session['role'] = role.name

            if role == Role.GAMER:
                wallet = authentication_repository.get_gamer_wallet(account_id)
                session['wallet'] = float(wallet)
                flash('Berhasil login!')
                return redirect(url_for('auth.gamer_homepage', gamer_id=account_id))  

            elif role == Role.ADMIN:
                flash('Berhasil login sebagai admin!')
                return render_template(f'{role.name.lower()}/admin_homepage.html', username=name, role=role.name)

            elif role == Role.PUBLISHER:
                flash('Berhasil login sebagai publisher!')
                return render_template(f'{role.name.lower()}/publisher_homepage.html', username=name, role=role.name)

        flash('Email tidak ditemukan.')
        return redirect(url_for('auth.login_controller'))

    return render_template('login.html')

def logout_controller():
    session.clear()
    return redirect(url_for('auth.login_controller'))