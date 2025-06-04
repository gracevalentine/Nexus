from shared.database import get_db_connection

def get_all_games():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT g.game_id, g.game_name, g.game_desc, g.game_price, g.game_image, a.name FROM game g JOIN account a ON g.publisher_id = a.id')
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
