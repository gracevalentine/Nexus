from flask import render_template, request, jsonify, flash, redirect, url_for
from model.Game import Game
from order.repo.order_repository import GamerRepo
import base64

class GamerController:

    @staticmethod
    def library(gamer_id):
        rows = GamerRepo.get_library_games(gamer_id)

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

    @staticmethod
    def storepage(gamer_id):
        rows = GamerRepo.get_all_games()  # pake method baru ambil semua game

        games = []
        for game_id, name, description, price, image_blob, publisher_name in rows:
            image_data = base64.b64encode(image_blob).decode('utf-8') if image_blob else None
            image_url = f"data:image/jpeg;base64,{image_data}" if image_data else "/static/asset/default.jpg"

            games.append({
                "id": game_id,
                "name": name,
                # "genre": genre,
                "description": description,
                "price": price,
                "publisher": publisher_name,
                "image": image_url
            })

        return render_template('gamer_stores.html', gamer_id=gamer_id, games=games)

    @staticmethod
    def genre_detail(genre, gamer_id):
        rows = GamerRepo.get_games_by_genre(genre)

        games = []
        for game_id, name, description, price, image_blob, publisher in rows:
            image_data = base64.b64encode(image_blob).decode('utf-8') if image_blob else None
            image_url = f"data:image/jpeg;base64,{image_data}" if image_data else "/static/asset/default.jpg"

            games.append({
                "id": game_id,
                "name": name,
                "description": description,
                "price": price,
                "publisher": publisher,
                "image": image_url
            })

        return render_template('gamer_stores.html', genre=genre, gamer_id=gamer_id, games=games)

    @staticmethod
    def buy_game(gamer_id, game_id):
        # Check owned
        if GamerRepo.check_game_owned(gamer_id, game_id):
            return jsonify({"status": "error", "message": "Game sudah dimiliki"})

        price = GamerRepo.get_game_price(game_id)
        if price is None:
            return jsonify({"status": "error", "message": "Game tidak ditemukan"})

        balance = GamerRepo.get_wallet_balance(gamer_id)
        if balance < price:
            return jsonify({"status": "error", "message": "Saldo tidak cukup"})

        try:
            order_id = GamerRepo.create_game_order(gamer_id)
            GamerRepo.insert_order_detail(order_id, game_id)
            GamerRepo.update_wallet_balance(gamer_id, balance - price)
            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

    @staticmethod
    def uninstall_game(gamer_id, game_id):
        try:
            GamerRepo.uninstall_game(gamer_id, game_id)
            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

    @staticmethod
    def show_cart(gamer_id):
        rows = GamerRepo.get_cart_games(gamer_id)

        games = []
        for row in rows:
            image_data = base64.b64encode(row['game_image']).decode('utf-8') if row['game_image'] else None
            image_url = f"data:image/jpeg;base64,{image_data}" if image_data else "/static/asset/default.jpg"
            game = Game(
                game_id=row['game_id'],
                name=row['game_name'],
                description=row.get('game_desc', ''),
                genre=row['game_genre'],
                price=row['game_price'],
                publisher_id=row['publisher_id']
            )
            game.cover_url = image_url
            games.append(game)

        return render_template("gamer_cart.html", gamer_id=gamer_id, cart_items=games)

    @staticmethod
    def add_to_cart(gamer_id, game_id):
        if GamerRepo.is_game_owned(gamer_id, game_id):
            return jsonify({"status": "error", "message": "Game sudah kamu miliki."})

        if GamerRepo.is_game_in_cart(gamer_id, game_id):
            return jsonify({"status": "error", "message": "Game sudah ada di cart."})

        try:
            GamerRepo.add_game_to_cart(gamer_id, game_id)
            return jsonify({"status": "success", "message": "Game berhasil ditambahkan ke cart!"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

    @staticmethod
    def remove_from_cart(gamer_id, game_id):
        try:
            GamerRepo.remove_game_from_cart(gamer_id, game_id)
            # redirect handled by route
        except Exception as e:
            flash(f"Gagal menghapus game dari cart: {str(e)}")

    @staticmethod
    def checkout(gamer_id, selected_game_ids):
        if not selected_game_ids:
            flash("Pilih dulu game yang ingin di-checkout.")
            return redirect(url_for('gamer.show_cart', gamer_id=gamer_id))

        selected_games = GamerRepo.get_selected_games(selected_game_ids)
        if not selected_games:
            flash("Game tidak ditemukan.")
            return redirect(url_for('gamer.show_cart', gamer_id=gamer_id))

        owned_games_rows = GamerRepo.get_owned_games(gamer_id, selected_game_ids)
        owned_games = {row['game_id'] for row in owned_games_rows}

        to_checkout = [g for g in selected_games if g['game_id'] not in owned_games]
        if not to_checkout:
            flash("Semua game yang dipilih sudah kamu miliki.")
            return redirect(url_for('gamer.show_cart', gamer_id=gamer_id))

        total_price = sum(float(g['game_price']) for g in to_checkout)
        wallet = GamerRepo.get_wallet_balance(gamer_id)

        if wallet < total_price:
            flash(f"Saldo tidak cukup. Total harga: Rp{int(total_price):,}, saldo kamu: Rp{int(wallet):,}")
            return redirect(url_for('gamer.show_cart', gamer_id=gamer_id))

        try:
            # Insert ke library & hapus dari cart
            GamerRepo.add_games_to_library_and_remove_from_cart(gamer_id, [g['game_id'] for g in to_checkout])

            # Kurangi saldo
            GamerRepo.update_wallet_balance(gamer_id, wallet - total_price)

            flash("Checkout berhasil! Game sudah masuk ke library kamu.")
            return redirect(url_for('gamer.gamer_library', gamer_id=gamer_id))
        except Exception as e:
            flash(f"Gagal checkout: {str(e)}")
            return redirect(url_for('gamer.show_cart', gamer_id=gamer_id))

    @staticmethod
    def add_review(gamer_id, game_id, review_text):
        if not review_text:
            return jsonify({"status": "error", "message": "Review kosong!"})

        try:
            GamerRepo.add_review(review_text, gamer_id, game_id)
            return jsonify({"status": "success"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

    @staticmethod
    def get_reviews(game_id):
        rows = GamerRepo.get_reviews(game_id)
        result = [{"review": r[0], "name": r[1], "gamer_id": r[2]} for r in rows]
        return jsonify(reviews=result)
