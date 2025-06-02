from shared.database import get_db_connection

class GamerRepository:
    @staticmethod
    def get_wallet_balance(gamer_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM gamer_wallet WHERE account_id = %s", (gamer_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return int(result[0]) if result else 0
    
    @staticmethod
    def get_owned_games(gamer_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT g.game_id, g.name, g.price, g.image_url
            FROM game g
            INNER JOIN gamer_game gg ON g.game_id = gg.game_id
            WHERE gg.account_id = %s
        """
        cursor.execute(query, (gamer_id,))
        games = cursor.fetchall()
        cursor.close()
        conn.close()
        return games

    @staticmethod
    def get_unowned_games(gamer_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT g.game_id, g.name, g.price, g.image_url
            FROM game g
            WHERE g.game_id NOT IN (
                SELECT gg.game_id
                FROM gamer_game gg
                WHERE gg.account_id = %s
            )
        """
        cursor.execute(query, (gamer_id,))
        games = cursor.fetchall()
        cursor.close()
        conn.close()
        return games

    @staticmethod
    def buy_game(gamer_id, game_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO gamer_game (account_id, game_id) VALUES (%s, %s)"
        cursor.execute(query, (gamer_id, game_id))
        conn.commit()
        cursor.close()
        conn.close()