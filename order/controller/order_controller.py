from flask import render_template, request, jsonify, flash, redirect, url_for, session
from organize_game.model.Game import Game
from order.repo import order_repository
import base64

def library(gamer_id):
    rows = order_repository.get_library_games(gamer_id)

    games = []
    for game_id, name, genre, image_blob in rows:
        image = base64.b64encode(image_blob).decode('utf-8') if image_blob else None
        image_url = f"data:image/jpeg;base64,{image}" if image else "/static/asset/default.jpg"
        games.append({
            "id": game_id,
            "name": name,
            "genre": genre,
            "image": image_url
        })

    return render_template("gamer_library.html", gamer_id=gamer_id, games=games)

def buy_game(gamer_id, game_id):
    if order_repository.check_game_owned(gamer_id, game_id):
        return jsonify({"status": "error", "message": "Game sudah dimiliki"})

    price = order_repository.get_game_price(game_id)
    if price is None:
        return jsonify({"status": "error", "message": "Game tidak ditemukan"})

    balance = order_repository.get_wallet_balance(gamer_id)
    if balance < price:
        return jsonify({"status": "error", "message": "Saldo tidak cukup"})

    try:
        order = order_repository.create_game_order(gamer_id)  # Ini sudah objek Order
        order_repository.insert_order_detail(order.order_id, game_id)  # Ambil order_id-nya
        order_repository.update_wallet_balance(gamer_id, balance - price)

        order_repository.add_to_library(gamer_id, game_id)

        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def uninstall_game(gamer_id, game_id):
    try:
        order_repository.uninstall_game(gamer_id, game_id)  # hapus dari order_detail
        order_repository.remove_from_library(gamer_id, game_id)  # hapus dari library
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def show_cart(gamer_id):
    rows = order_repository.get_cart_games(gamer_id)

    games = []
    for row in rows:
        game_info = row["game"]

        image_blob = game_info.get("game_image")
        if image_blob:
            image_data = base64.b64encode(image_blob).decode('utf-8')
            image_url = f"data:image/jpeg;base64,{image_data}"
        else:
            image_url = "/static/asset/default.jpg"

        # **PENTING**: jangan lupa kirim status ke Game() juga, kalau nggak bakal error!
        game = Game(
            game_id=game_info.get("game_id"),
            name=game_info.get("game_name"),
            description=game_info.get("game_desc", ''),
            genre=game_info.get("game_genre", ''),
            price=game_info.get("game_price", 0),
            publisher_id=game_info.get("publisher_id"),
            status=game_info.get("game_status", 0)  # default 0 atau sesuaikan
        )
        game.cover_url = image_url

        games.append(game)

    return render_template("gamer_cart.html", gamer_id=gamer_id, cart_items=games)

def add_to_cart(gamer_id, game_id):
    if 'username' not in session:
        return jsonify({"status": "error", "message": "Session habis. Silakan login ulang."})
    
    if order_repository.is_game_owned(gamer_id, game_id):
        return jsonify({"status": "error", "message": "Game sudah kamu miliki."})

    if order_repository.is_game_in_cart(gamer_id, game_id):
        return jsonify({"status": "error", "message": "Game sudah ada di cart."})

    try:
        order_repository.add_game_to_cart(gamer_id, game_id)
        return jsonify({"status": "success", "message": "Game berhasil ditambahkan ke cart!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def remove_from_cart(gamer_id, game_id):
    try:
        order_repository.remove_game_from_cart(gamer_id, game_id)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def checkout(gamer_id):
    selected_game_ids = request.form.getlist("selected_game_ids")
    if not selected_game_ids:
        flash("Pilih dulu game yang ingin di-checkout.")
        return redirect(url_for('order.show_cart', gamer_id=gamer_id))

    selected_games = order_repository.get_selected_games(selected_game_ids)
    if not selected_games:
        flash("Game tidak ditemukan.")
        return redirect(url_for('order.show_cart', gamer_id=gamer_id))

    owned_games_rows = order_repository.get_owned_games(gamer_id, selected_game_ids)
    owned_games = {row[0] for row in owned_games_rows}

    to_checkout = [g for g in selected_games if g['game_id'] not in owned_games]
    if not to_checkout:
        flash("Semua game yang dipilih sudah kamu miliki.")
        return redirect(url_for('order.show_cart', gamer_id=gamer_id))

    total_price = sum(float(g['game_price']) for g in to_checkout)
    wallet = order_repository.get_wallet_balance(gamer_id)

    if wallet < total_price:
        flash(f"Saldo tidak cukup. Total harga: Rp{int(total_price):,}, saldo kamu: Rp{int(wallet):,}")
        return redirect(url_for('order.show_cart', gamer_id=gamer_id))

    try:
        order_repository.add_games_to_library_and_remove_from_cart(gamer_id, [g['game_id'] for g in to_checkout])
        order_repository.update_wallet_balance(gamer_id, wallet - total_price)

        flash("Checkout berhasil! Game sudah masuk ke library kamu.")
        return redirect(url_for('order.library', gamer_id=gamer_id))
    except Exception as e:
        flash(f"Gagal checkout: {str(e)}")
        return redirect(url_for('order.show_cart', gamer_id=gamer_id))