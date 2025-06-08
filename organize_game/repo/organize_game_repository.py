from shared.database import get_db_connection
from organize_game.model.Game import Game

def get_games_by_publisher(publisher_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM game WHERE publisher_id = %s", (publisher_id,))
    games_data = cursor.fetchall()
    cursor.close()
    db.close()

    return [Game(
        game_id=game['game_id'],
        name=game['game_name'],
        description=game['game_desc'],
        genre=game['game_genre'],
        price=game['game_price'],
        publisher_id=game['publisher_id'],
        status=game['game_status'],
        image=game.get('game_image')
    ) for game in games_data]

def insert_game(game_data):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        '''INSERT INTO game (game_name, game_desc, game_genre, game_price, game_image, game_status, publisher_id)
           VALUES (%s, %s, %s, %s, %s, %s, %s)''',
        game_data
    )
    db.commit()
    cursor.close()
    db.close()

def get_game_by_id(game_id, publisher_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM game WHERE game_id = %s AND publisher_id = %s", (game_id, publisher_id))
    game_data = cursor.fetchone()
    cursor.close()
    db.close()

    if game_data:
        return Game(
            game_id=game_data['game_id'],
            name=game_data['game_name'],
            description=game_data['game_desc'],
            genre=game_data['game_genre'],
            price=game_data['game_price'],
            publisher_id=game_data['publisher_id'],
            status=game_data['game_status'],
            image=game_data.get('game_image')
        )
    return None

def update_game(game_id, publisher_id, data, with_image=False):
    db = get_db_connection()
    cursor = db.cursor()
    if with_image:
        cursor.execute("""
            UPDATE game SET game_name=%s, game_price=%s, game_genre=%s, game_desc=%s, game_image=%s, game_status=%s
            WHERE game_id=%s AND publisher_id=%s
        """, (*data, game_id, publisher_id))
    else:
        cursor.execute("""
            UPDATE game SET game_name=%s, game_price=%s, game_genre=%s, game_desc=%s, game_status=%s
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
