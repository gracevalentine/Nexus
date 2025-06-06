from shared.database import get_db_connection

def get_games_by_publisher(publisher_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM game WHERE publisher_id = %s", (publisher_id,))
    games = cursor.fetchall()
    cursor.close()
    db.close()
    return games

def insert_game(game_data):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        '''INSERT INTO game (game_name, game_desc, game_genre, game_price, game_image, publisher_id)
           VALUES (%s, %s, %s, %s, %s, %s)''',
        game_data
    )
    db.commit()
    cursor.close()
    db.close()

def get_game_by_id(game_id, publisher_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM game WHERE game_id = %s AND publisher_id = %s", (game_id, publisher_id))
    game = cursor.fetchone()
    cursor.close()
    db.close()
    return game

def update_game(game_id, publisher_id, data, with_image=False):
    db = get_db_connection()
    cursor = db.cursor()
    if with_image:
        cursor.execute("""
            UPDATE game SET game_name=%s, game_price=%s, game_genre=%s, game_desc=%s, game_image=%s
            WHERE game_id=%s AND publisher_id=%s
        """, (*data, game_id, publisher_id))
    else:
        cursor.execute("""
            UPDATE game SET game_name=%s, game_price=%s, game_genre=%s, game_desc=%s
            WHERE game_id=%s AND publisher_id=%s
        """, (*data, game_id, publisher_id))
    db.commit()
    cursor.close()
    db.close()

def delete_game(game_id, publisher_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('DELETE FROM game WHERE game_id = %s AND publisher_id = %s', (game_id, publisher_id))
    db.commit()
    cursor.close()
    db.close()
