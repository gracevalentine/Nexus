from multiprocessing import connection
from shared.database import get_db_connection
from datetime import datetime
from order.model.Order import Order
from organize_game.model.Game import Game 
from order.model.Cart import Cart

def get_library_games(gamer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT g.game_id, g.game_name, g.game_genre, g.game_image
        FROM library l
        JOIN game g ON l.game_id = g.game_id
        WHERE l.gamer_id = %s
    """, (gamer_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def add_to_library(gamer_id, game_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO library (gamer_id, game_id) VALUES (%s, %s)", (gamer_id, game_id))
    conn.commit()
    cursor.close()
    conn.close()


def get_all_games():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT g.game_id, g.game_name, g.game_desc, g.game_price, g.game_image, a.name
        FROM game g
        JOIN account a ON g.publisher_id = a.id
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    result = []
    for row in rows:
        game = Game(
            game_id=row[0],
            game_name=row[1],
            game_desc=row[2],
            game_price=row[3],
            game_image=row[4],
            publisher_name=row[5]
        )
        result.append(game)
    return result

def remove_from_library(gamer_id, game_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM library WHERE gamer_id = %s AND game_id = %s", (gamer_id, game_id))
    conn.commit()
    cursor.close()
    conn.close()


def get_store_genres():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT game_genre, game_image FROM game GROUP BY game_genre")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def get_games_by_genre(genre):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT g.game_id, g.game_name, g.game_desc, g.game_price, g.game_image, a.name
        FROM game g
        JOIN account a ON g.publisher_id = a.id
        WHERE g.game_genre = %s
    """, (genre,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def check_game_owned(gamer_id, game_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1 FROM order_detail od
        JOIN game_order go ON od.order_id = go.order_id
        WHERE go.gamer_id = %s AND od.game_id = %s
    """, (gamer_id, game_id))
    owned = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return owned


def get_game_price(game_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT game_price FROM game WHERE game_id = %s", (game_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return float(result[0]) if result else None


def get_wallet_balance(gamer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM gamer_wallet WHERE account_id = %s", (gamer_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return float(result[0]) if result else 0


def create_game_order(gamer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO game_order (gamer_id) VALUES (%s)", (gamer_id,))
    order_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return Order(order_id=order_id, gamer_id=gamer_id)

def insert_order_detail(order_id, game_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO order_detail (order_id, game_id, description)
        VALUES (%s, %s, %s)
    """, (order_id, game_id, "Pembelian game"))
    conn.commit()
    cursor.close()
    conn.close()

def update_wallet_balance(gamer_id, new_balance):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE gamer_wallet
        SET balance = %s
        WHERE account_id = %s
    """, (new_balance, gamer_id))
    conn.commit()
    cursor.close()
    conn.close()


def uninstall_game(gamer_id, game_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE od FROM order_detail od
        JOIN game_order go ON od.order_id = go.order_id
        WHERE go.gamer_id = %s AND od.game_id = %s
    """, (gamer_id, game_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_cart_games(gamer_id):
    query = """
        SELECT c.gamer_id, c.game_id, c.date_added,
               g.game_name, g.game_desc, g.game_genre, g.game_price, g.game_image, g.publisher_id
        FROM cart c
        JOIN game g ON c.game_id = g.game_id
        WHERE c.gamer_id = %s
    """

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, (gamer_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    result = []
    for row in rows:
        cart = Cart(row[0], row[1], row[2])
        game_info = {
            "game_id": row[1],
            "game_name": row[3],
            "game_desc": row[4],
            "game_genre": row[5],
            "game_price": row[6],
            "game_image": row[7],
            "publisher_id": row[8]
        }
        result.append({"cart": cart, "game": game_info})

    return result

def is_game_owned(gamer_id, game_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM library WHERE gamer_id = %s AND game_id = %s", (gamer_id, game_id))
    result = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return result


def is_game_in_cart(gamer_id, game_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM cart WHERE gamer_id = %s AND game_id = %s", (gamer_id, game_id))
    result = cursor.fetchone() is not None
    cursor.close()
    conn.close()
    return result


def add_game_to_cart(gamer_id, game_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cart (gamer_id, game_id, date_added)
        VALUES (%s, %s, %s)
    """, (gamer_id, game_id, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()


def remove_game_from_cart(gamer_id, game_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cart WHERE gamer_id = %s AND game_id = %s", (gamer_id, game_id))
    conn.commit()
    cursor.close()
    conn.close()


def get_selected_games(game_ids):
    conn = get_db_connection()
    cursor = conn.cursor()
    format_strings = ','.join(['%s'] * len(game_ids))
    cursor.execute(f"""
        SELECT game_id, game_price
        FROM game
        WHERE game_id IN ({format_strings})
    """, tuple(game_ids))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert to list of dicts
    return [{"game_id": row[0], "game_price": row[1]} for row in rows]

def get_owned_games(gamer_id, game_ids):
    conn = get_db_connection()
    cursor = conn.cursor()
    format_strings = ','.join(['%s'] * len(game_ids))
    cursor.execute(f"""
        SELECT game_id FROM library
        WHERE gamer_id = %s AND game_id IN ({format_strings})
    """, (gamer_id, *game_ids))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def add_games_to_library_and_remove_from_cart(gamer_id, game_ids):
    conn = get_db_connection()
    cursor = conn.cursor()
    for game_id in game_ids:
        cursor.execute("INSERT INTO library (gamer_id, game_id) VALUES (%s, %s)", (gamer_id, game_id))
        cursor.execute("DELETE FROM cart WHERE gamer_id = %s AND game_id = %s", (gamer_id, game_id))
    conn.commit()
    cursor.close()
    conn.close()

