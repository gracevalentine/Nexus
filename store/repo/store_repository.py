from shared.database import get_db_connection
from organize_game.model.Game import Game
from store.model.Review import Review
from datetime import datetime

def get_all_games():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            g.game_id, g.game_name, g.game_desc, g.game_genre, g.game_price, 
            g.publisher_id, g.game_image, a.name AS publisher_name
        FROM game g
        JOIN account a ON g.publisher_id = a.id
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    games = []
    for row in rows:
        # Buat objek Game biasa, tanpa image dan publisher_name
        game = Game(
            game_id=row['game_id'],
            name=row['game_name'],
            description=row['game_desc'],
            genre=row['game_genre'],
            price=row['game_price'],
            publisher_id=row['publisher_id']
        )

        # Sisipkan image_blob & publisher_name dalam dict (gak masuk Game)
        games.append({
            "game": game,  # object Game
            "image_blob": row['game_image'],
            "publisher_name": row['publisher_name']
        })
    return games



def get_games_by_genre(genre):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT game_id, game_name, game_desc, game_genre, game_price, publisher_id
        FROM game
        WHERE game_genre = %s
    """, (genre,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    games = []
    for row in rows:
        game = Game(
            game_id=row['game_id'],
            name=row['game_name'],
            description=row['game_desc'],
            genre=row['game_genre'],
            price=row['game_price'],
            publisher_id=row['publisher_id']
        )
        games.append(game)
    return games


def get_game_by_id(game_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT game_id, game_name, game_desc, game_genre, game_price, publisher_id
        FROM game
        WHERE game_id = %s
    """, (game_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        return Game(
            game_id=row['game_id'],
            name=row['game_name'],
            description=row['game_desc'],
            genre=row['game_genre'],
            price=row['game_price'],
            publisher_id=row['publisher_id']
        )
    return None


def add_review(review_text, gamer_id, game_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO review (review_text, reviewer, game_id)
        VALUES (%s, %s, %s)
    """, (review_text, gamer_id, game_id))
    conn.commit()
    cursor.close()
    conn.close()


def get_reviews(game_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            r.review_id,
            r.review_text,
            r.review_date,
            a.name AS reviewer,
            g.game_id, g.game_name, g.game_desc, g.game_genre, g.game_price, g.publisher_id
        FROM review r
        JOIN account a ON r.reviewer = a.id
        JOIN game g ON r.game_id = g.game_id
        WHERE r.game_id = %s
        ORDER BY r.review_date DESC
    """, (game_id,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    reviews = []
    for row in rows:
        game = Game(
            game_id=row['game_id'],
            name=row['game_name'],
            description=row['game_desc'],
            genre=row['game_genre'],
            price=row['game_price'],
            publisher_id=row['publisher_id']
        )

        # Pastikan review_date valid
        if isinstance(row['review_date'], str):
            try:
                review_date = datetime.strptime(row['review_date'], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                review_date = datetime.now()
        else:
            review_date = row['review_date']

        review = Review(
            review_id=row['review_id'],
            review_text=row['review_text'],
            game=game,
            reviewer=row['reviewer'],
            date=review_date
        )
        reviews.append(review)
    return reviews
