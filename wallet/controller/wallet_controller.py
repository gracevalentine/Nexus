from flask import render_template, request, flash, redirect, session, url_for, jsonify
from wallet.repo import wallet_repository

def walletpage(gamer_id):
    if 'username' not in session:
        return redirect(url_for('auth.login_controller'))

    wallet_balance = wallet_repository.get_wallet_balance(gamer_id)
    
    if wallet_balance is None:
        flash("Gagal mengambil saldo wallet.", "error")
        return redirect(url_for('gamer.storepage', gamer_id=gamer_id))

    # dummy transaksi sementara
    transactions = []  # bisa diganti kalau udah ada tabel transaksi

    return render_template('gamer_wallet.html', gamer_id=gamer_id, wallet_balance=wallet_balance, transactions=transactions)

def topup_wallet(gamer_id):
    if 'username' not in session:
        return redirect(url_for('auth.login_controller'))

    data = request.get_json()
    amount = data.get('amount', 0)

    if amount < 1000:
        return jsonify({"status": "error", "message": "Minimal top up Rp 1.000"})

    success = wallet_repository.topup_wallet(gamer_id, amount)

    if success:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Top up gagal. Akun tidak ditemukan."})
