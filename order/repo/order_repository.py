from controller.db_controller import get_db_connection
import base64

class GamerRepo:

    @staticmethod
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

    @staticmethod
    def get_all_games():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT g.game_id, g.game_name, g.game_desc, g.game_price, g.game_image, a.name FROM game g JOIN account a ON g.publisher_id = a.id')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def get_store_genres():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT game_genre, game_image FROM game GROUP BY game_genre')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
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

    @staticmethod
    def check_game_owned(gamer_id, game_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 1 FROM order_detail od
            JOIN game_order go ON od.order_id = go.order_id
            WHERE go.gamer_id = %s AND od.game_id = %s
        ''', (gamer_id, game_id))
        owned = cursor.fetchone() is not None
        cursor.close()
        conn.close()
        return owned

    @staticmethod
    def get_game_price(game_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT game_price FROM game WHERE game_id = %s", (game_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return float(result[0]) if result else None

    @staticmethod
    def get_wallet_balance(gamer_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM gamer_wallet WHERE account_id = %s", (gamer_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return float(result[0]) if result else 0

    @staticmethod
    def create_game_order(gamer_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO game_order (gamer_id) VALUES (%s)", (gamer_id,))
        order_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return order_id

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def get_cart_games(gamer_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT g.*
            FROM cart c
            JOIN game g ON c.game_id = g.game_id
            WHERE c.gamer_id = %s
        """, (gamer_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def is_game_owned(gamer_id, game_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM library WHERE gamer_id = %s AND game_id = %s", (gamer_id, game_id))
        result = cursor.fetchone() is not None
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def is_game_in_cart(gamer_id, game_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM cart WHERE gamer_id = %s AND game_id = %s", (gamer_id, game_id))
        result = cursor.fetchone() is not None
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def add_game_to_cart(gamer_id, game_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cart (gamer_id, game_id) VALUES (%s, %s)", (gamer_id, game_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def remove_game_from_cart(gamer_id, game_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE gamer_id = %s AND game_id = %s", (gamer_id, game_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_selected_games(game_ids):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        format_strings = ','.join(['%s'] * len(game_ids))
        cursor.execute(f"""
            SELECT g.game_id, g.game_price
            FROM game g
            WHERE g.game_id IN ({format_strings})
        """, tuple(game_ids))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def get_owned_games(gamer_id, game_ids):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        format_strings = ','.join(['%s'] * len(game_ids))
        cursor.execute(f"""
            SELECT game_id FROM library
            WHERE gamer_id = %s AND game_id IN ({format_strings})
        """, (gamer_id, *game_ids))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @staticmethod
    def add_games_to_library_and_remove_from_cart(gamer_id, game_ids):
        conn = get_db_connection()
        cursor = conn.cursor()
        for game_id in game_ids:
            cursor.execute("INSERT INTO library (gamer_id, game_id) VALUES (%s, %s)", (gamer_id, game_id))
            cursor.execute("DELETE FROM cart WHERE gamer_id = %s AND game_id = %s", (gamer_id, game_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def add_review(review_text, reviewer, game_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO review (review_text, reviewer, game_id) VALUES (%s, %s, %s)",
            (review_text, reviewer, game_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
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
        cursor.close()
        conn.close()
        return rows
