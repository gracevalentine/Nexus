from flask import Blueprint, render_template, request, redirect, url_for, flash
from PIL import Image  
import io
import base64
from controller.db_controller import get_db_connection 

publisher_bp = Blueprint('publisher', __name__, url_prefix='/publisher')

@publisher_bp.route('/dashboard/<int:publisher_id>')
def publisher_homepage(publisher_id):
    return render_template('publisher_homepage.html', publisher_id=publisher_id)

@publisher_bp.route('/publishedgames/<int:publisher_id>')
def published_games(publisher_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM game WHERE publisher_id = %s", (publisher_id,))
    games = cursor.fetchall()

    for game in games:
        if game['game_image']:
            game['image_data'] = base64.b64encode(game['game_image']).decode('utf-8')
        else:
            game['image_data'] = None

    return render_template('published_games.html', games=games, publisher_id=publisher_id)


@publisher_bp.route('/addgame/<int:publisher_id>', methods=['GET', 'POST'])
def add_new_game(publisher_id):
    if request.method == 'POST':
        game_name = request.form['game-name']
        description = request.form['description']
        genre = request.form['genre']
        price = request.form['price-game']
        image_file = request.files.get('image')

        image_data = None
        if image_file:

            img = Image.open(image_file)
            img.thumbnail((600, 600))  # Resize max 600x600

            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            image_data = buffer.getvalue()

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            '''INSERT INTO game (game_name, game_desc, game_genre, game_price, game_image, publisher_id)
               VALUES (%s, %s, %s, %s, %s, %s)''',
            (game_name, description, genre, price, image_data, publisher_id)
        )
        db.commit()

        flash('Game successfully added!')
        return redirect(url_for('publisher.published_games', publisher_id=publisher_id))
    
    return render_template('publisher_new_game.html', publisher_id=publisher_id)


@publisher_bp.route('/edit_game/<int:publisher_id>/<int:game_id>', methods=['GET', 'POST'])
def edit_game(publisher_id, game_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['game-name']
        price = request.form['price-game']
        genre = request.form['genre']
        desc = request.form['description']
        image_file = request.files.get('image')

        if image_file and image_file.filename != '':
            image_data = image_file.read()
            cursor.execute("""
                UPDATE game SET game_name=%s, game_price=%s, game_genre=%s, game_desc=%s, game_image=%s
                WHERE game_id=%s AND publisher_id=%s
            """, (name, price, genre, desc, image_data, game_id, publisher_id))
        else:
            cursor.execute("""
                UPDATE game SET game_name=%s, game_price=%s, game_genre=%s, game_desc=%s
                WHERE game_id=%s AND publisher_id=%s
            """, (name, price, genre, desc, game_id, publisher_id))

        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('publisher.published_games', publisher_id=publisher_id))

    # GET request
    cursor.execute("SELECT * FROM game WHERE game_id = %s AND publisher_id = %s", (game_id, publisher_id))
    game = cursor.fetchone()

    if game and game['game_image']:
        game['image_data'] = base64.b64encode(game['game_image']).decode('utf-8')

    cursor.close()
    conn.close()
    return render_template('publisher_new_game.html', 
                           is_edit=True,
                           form_action=url_for('publisher.edit_game', publisher_id=publisher_id, game_id=game_id),
                           game=game,
                           publisher_id=publisher_id)

@publisher_bp.route('/deletegame/<int:publisher_id>/<int:game_id>', methods=['POST'])
def delete_game(publisher_id, game_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('SELECT * FROM game WHERE game_id = %s AND publisher_id = %s', (game_id, publisher_id))
    game = cursor.fetchone()

    if game:
        cursor.execute('DELETE FROM game WHERE game_id = %s', (game_id,))
        conn.commit()

    cursor.close()
    conn.close()
    return redirect(url_for('publisher.published_games', publisher_id=publisher_id))
