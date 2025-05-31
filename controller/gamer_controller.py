from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
# from flask import Blueprint, render_template, request, redirect, url_for
from model.Gamer import Gamer
from model.Cart import Cart
from model.Game import Game
from controller.db_controller import get_db_connection 
import base64

gamer_bp = Blueprint('gamer', __name__, url_prefix='/gamer')

@gamer_bp.route('/dashboard/<int:gamer_id>')
def gamer_homepage(gamer_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM gamer_wallet WHERE account_id = %s", (gamer_id,))
    result = cursor.fetchone()
    balance = int(result[0]) if result else 0

    cursor.close()
    conn.close()

    return render_template("home_page.html", gamer_id=gamer_id, wallet_balance=balance)

@gamer_bp.route('/library/<int:gamer_id>')
def gamer_library(gamer_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT g.game_id, g.game_name, g.game_genre, g.game_image
        FROM library l
        JOIN game g ON l.game_id = g.game_id
        WHERE l.gamer_id = %s
    """, (gamer_id,))
    rows = cursor.fetchall()

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

    cursor.close()
    conn.close()

    return render_template("library.html", gamer_id=gamer_id, games=games)


@gamer_bp.route('/storepage/<int:gamer_id>')
def gamer_storepage(gamer_id):
    # Connect DB
    conn = get_db_connection()
    cursor = conn.cursor()

    # Ambil 1 game per genre (pakai MIN(game_id))
    query = '''
        SELECT game_genre, game_image
        FROM game
        GROUP BY game_genre
    '''
    cursor.execute(query)
    rows = cursor.fetchall()

    # Format jadi genre + base64 image
    genre_cards = []
    for genre, blob in rows:
        if blob:  # pastikan gambar ada
            encoded_image = base64.b64encode(blob).decode('utf-8')
            image_data_uri = f"data:image/jpeg;base64,{encoded_image}"
            genre_cards.append({
                "name": genre,
                "image": image_data_uri
            })

    cursor.close()
    conn.close()

    return render_template('store_page.html', gamer_id=gamer_id, genre_cards=genre_cards)

@gamer_bp.route('/storepage/genre/<genre>/<int:gamer_id>')
def genre_detail(genre, gamer_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = '''
        SELECT g.game_id, g.game_name, g.game_desc, g.game_price, g.game_image, a.name
        FROM game g
        JOIN account a ON g.publisher_id = a.id
        WHERE g.game_genre = %s
    '''
    cursor.execute(query, (genre,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

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

    return render_template('games_detail_page.html', genre=genre, gamer_id=gamer_id, games=games)

@gamer_bp.route('/wallet/<int:gamer_id>')
def wallet_page(gamer_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Ambil saldo
    cursor.execute("SELECT balance FROM gamer_wallet WHERE account_id = %s", (gamer_id,))
    result = cursor.fetchone()
    wallet_balance = result[0] if result else 0

    gamer = Gamer(name="", password="", id=gamer_id)  # nama & pw bisa dikosongin kalau gak dipakai
    gamer.wallet = wallet_balance

    # Ambil transaksi
    cursor.execute("""
        SELECT od.order_date, g.game_name, g.game_price
        FROM order_detail od
        JOIN game_order go ON od.order_id = go.order_id
        JOIN game g ON od.game_id = g.game_id
        WHERE go.gamer_id = %s
        ORDER BY od.order_date DESC
    """, (gamer_id,))
    rows = cursor.fetchall()

    transactions = []
    for date, game_name, price in rows:
        transactions.append({
            "date": date.strftime("%Y-%m-%d"),
            "description": f"Beli {game_name}",
            "amount": -float(price)
        })

    gamer.games = transactions  # contoh: bisa disimpan juga di properti `games`

    cursor.close()
    conn.close()

    return render_template(
        "gamer_wallet.html",
        gamer_id=gamer_id,
        wallet_balance=int(gamer.wallet),  # pakai getter
        transactions=gamer.games            # pakai getter
    )

@gamer_bp.route('/wallet/topup/<int:gamer_id>', methods=['POST'])
def topup_wallet(gamer_id):
    data = request.get_json()
    amount = data.get('amount')

    if not amount or amount < 1000:
        return jsonify({"status": "error", "message": "Jumlah minimal top up Rp 1.000"})

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Update saldo di gamer_wallet
        cursor.execute("""
            UPDATE gamer_wallet
            SET balance = balance + %s
            WHERE account_id = %s
        """, (amount, gamer_id))

        conn.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()
    
@gamer_bp.route('/buy/<int:gamer_id>/<int:game_id>', methods=['POST'])
def buy_game(gamer_id, game_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Cek apakah game sudah dimiliki
        cursor.execute('''
            SELECT 1 FROM order_detail od
            JOIN game_order go ON od.order_id = go.order_id
            WHERE go.gamer_id = %s AND od.game_id = %s
        ''', (gamer_id, game_id))
        if cursor.fetchone():
            return jsonify({"status": "error", "message": "Game sudah dimiliki"})

        cursor.execute("SELECT game_price FROM game WHERE game_id = %s", (game_id,))
        result = cursor.fetchone()
        if not result:
            return jsonify({"status": "error", "message": "Game tidak ditemukan"})

        price = float(result[0])

        cursor.execute("SELECT balance FROM gamer_wallet WHERE account_id = %s", (gamer_id,))
        result = cursor.fetchone()
        if not result or result[0] < price:
            return jsonify({"status": "error", "message": "Saldo tidak cukup"})

        cursor.execute("INSERT INTO game_order (gamer_id) VALUES (%s)", (gamer_id,))
        order_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO order_detail (order_id, game_id, description)
            VALUES (%s, %s, %s)
        """, (order_id, game_id, "Pembelian game"))

        cursor.execute("""
            UPDATE gamer_wallet
            SET balance = balance - %s
            WHERE account_id = %s
        """, (price, gamer_id))

        conn.commit()
        return jsonify({"status": "success"})

    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)})

    finally:
        cursor.close()
        conn.close()

@gamer_bp.route('/uninstall/<int:gamer_id>/<int:game_id>', methods=['POST'])
def uninstall_game(gamer_id, game_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE od FROM order_detail od
            JOIN game_order go ON od.order_id = go.order_id
            WHERE go.gamer_id = %s AND od.game_id = %s
        """, (gamer_id, game_id))

        conn.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()
        
@gamer_bp.route('/cart/<int:gamer_id>')
def show_cart(gamer_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT g.*
        FROM cart c
        JOIN game g ON c.game_id = g.game_id
        WHERE c.gamer_id = %s
    """, (gamer_id,))
    rows = cursor.fetchall()

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

    cursor.close()
    conn.close()

    return render_template("cart.html", gamer_id=gamer_id, cart_items=games)

from flask import jsonify

@gamer_bp.route('/cart/add/<int:gamer_id>/<int:game_id>', methods=['POST'])
def add_to_cart(gamer_id, game_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Cek kalau game sudah pernah dibeli
        cursor.execute("SELECT 1 FROM library WHERE gamer_id = %s AND game_id = %s", (gamer_id, game_id))
        if cursor.fetchone():
            return jsonify({"status": "error", "message": "Game sudah kamu miliki."})

        # Cek kalau game sudah ada di cart
        cursor.execute("SELECT 1 FROM cart WHERE gamer_id = %s AND game_id = %s", (gamer_id, game_id))
        if cursor.fetchone():
            return jsonify({"status": "error", "message": "Game sudah ada di cart."})

        # Insert ke cart
        cursor.execute("INSERT INTO cart (gamer_id, game_id) VALUES (%s, %s)", (gamer_id, game_id))
        conn.commit()

        return jsonify({"status": "success", "message": "Game berhasil ditambahkan ke cart!"})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

    finally:
        cursor.close()
        conn.close()


@gamer_bp.route('/cart/remove/<int:gamer_id>/<int:game_id>', methods=['POST'])
def remove_from_cart(gamer_id, game_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cart WHERE gamer_id = %s AND game_id = %s", (gamer_id, game_id))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Game berhasil dihapus dari keranjang!")
    return redirect(url_for('gamer.show_cart', gamer_id=gamer_id))

@gamer_bp.route('/cart/checkout/<int:gamer_id>', methods=['POST'])
def checkout(gamer_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Ambil game yang dipilih dari form
        selected_game_ids = request.form.getlist('selected_games')

        if not selected_game_ids:
            flash("Pilih dulu game yang ingin di-checkout.")
            return redirect(url_for('gamer.show_cart', gamer_id=gamer_id))

        # Konversi jadi int
        selected_game_ids = [int(gid) for gid in selected_game_ids]

        # Ambil daftar game yang dipilih + harga
        format_strings = ','.join(['%s'] * len(selected_game_ids))
        cursor.execute(f"""
            SELECT g.game_id, g.game_price
            FROM game g
            WHERE g.game_id IN ({format_strings})
        """, tuple(selected_game_ids))
        selected_games = cursor.fetchall()

        if not selected_games:
            flash("Game tidak ditemukan.")
            return redirect(url_for('gamer.show_cart', gamer_id=gamer_id))

        # Ambil daftar game yang udah dimiliki
        cursor.execute(f"""
            SELECT game_id FROM library
            WHERE gamer_id = %s AND game_id IN ({format_strings})
        """, (gamer_id, *selected_game_ids))
        owned_games = {row['game_id'] for row in cursor.fetchall()}

        # Filter hanya game yang belum dimiliki
        to_checkout = [g for g in selected_games if g['game_id'] not in owned_games]
        if not to_checkout:
            flash("Semua game yang dipilih sudah kamu miliki.")
            return redirect(url_for('gamer.show_cart', gamer_id=gamer_id))

        total_price = sum(float(g['game_price']) for g in to_checkout)

        # Cek saldo
        cursor.execute("SELECT balance FROM gamer_wallet WHERE account_id = %s", (gamer_id,))
        wallet_row = cursor.fetchone()
        wallet = float(wallet_row['balance']) if wallet_row else 0

        if wallet < total_price:
            flash(f"Saldo tidak cukup. Total harga: Rp{int(total_price):,}, saldo kamu: Rp{int(wallet):,}")
            return redirect(url_for('gamer.show_cart', gamer_id=gamer_id))

        # Proses pembelian
        for game in to_checkout:
            game_id = game['game_id']
            print(f"🔁 Insert ke library: gamer_id={gamer_id}, game_id={game_id}")
            
            try:
                cursor.execute("INSERT INTO library (gamer_id, game_id) VALUES (%s, %s)", (gamer_id, game_id))
                cursor.execute("DELETE FROM cart WHERE gamer_id = %s AND game_id = %s", (gamer_id, game_id))
            except Exception as err:
                print(f"❌ Gagal insert game ke library: {err}")

        # Kurangi saldo
        new_wallet = wallet - total_price
        cursor.execute("UPDATE gamer_wallet SET balance = %s WHERE account_id = %s", (new_wallet, gamer_id))

        conn.commit()
        flash("Checkout berhasil! Game sudah masuk ke library kamu.")
        return redirect(url_for('gamer.gamer_library', gamer_id=gamer_id))

    except Exception as e:
        conn.rollback()
        flash(f"Gagal checkout: {str(e)}")
        return redirect(url_for('gamer.show_cart', gamer_id=gamer_id))

    finally:
        cursor.close()
        conn.close()

@gamer_bp.route('/review/<int:gamer_id>/<int:game_id>', methods=['POST'])
def add_review(gamer_id, game_id):
    data = request.get_json()
    review_text = data.get('review')

    if not review_text:
        return jsonify({"status": "error", "message": "Review kosong!"})

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO review (review_text, reviewer, game_id) VALUES (%s, %s, %s)",
            (review_text, gamer_id, game_id)
        )
        conn.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()


@gamer_bp.route('/gamer/review/list/<int:game_id>')
def get_reviews(game_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT r.review_text, a.username, r.reviewer
        FROM review r
        JOIN account a ON r.reviewer = a.id
        WHERE r.game_id = %s
        ORDER BY r.review_date DESC
    """, (game_id,))
    rows = cursor.fetchall()

    result = [{"review": r[0], "name": r[1], "gamer_id": r[2]} for r in rows]

    cursor.close()
    conn.close()

    return jsonify(reviews=result)