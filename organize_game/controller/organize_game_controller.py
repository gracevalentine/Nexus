# from tkinter import Image
from flask import render_template, request, redirect, session, url_for, flash
from PIL import Image
import base64
import io
from organize_game.repo import organize_game_repository

def publisher_homepage(publisher_id):
    publisher_id = session.get('publisher_id')
    return render_template('publisher_homepage.html', publisher_id=publisher_id, username=session.get('username', 'Publisher'))

def published_games(publisher_id):
    games = organize_game_repository.get_games_by_publisher(publisher_id)
    for game in games:
        if game['game_image']:
            game['image_data'] = base64.b64encode(game['game_image']).decode('utf-8')
        else:
            game['image_data'] = None
    return render_template('published_games.html', games=games, publisher_id=publisher_id)

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
            img.thumbnail((600, 600))
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=85)
            image_data = buffer.getvalue()

        organize_game_repository.insert_game((game_name, description, genre, price, image_data, publisher_id))
        flash('Game successfully added!')
        return redirect(url_for('published_games', publisher_id=publisher_id))

    return render_template('publisher_new_game.html', publisher_id=publisher_id)

def edit_game(publisher_id, game_id):
    if request.method == 'POST':
        name = request.form['game-name']
        price = request.form['price-game']
        genre = request.form['genre']
        desc = request.form['description']
        image_file = request.files.get('image')

        if image_file and image_file.filename != '':
            image_data = image_file.read()
            organize_game_repository.update_game(game_id, publisher_id, (name, price, genre, desc, image_data), with_image=True)
        else:
            organize_game_repository.update_game(game_id, publisher_id, (name, price, genre, desc), with_image=False)

        return redirect(url_for('published_games', publisher_id=publisher_id))

    game = organize_game_repository.get_game_by_id(game_id, publisher_id)
    if game and game['game_image']:
        game['image_data'] = base64.b64encode(game['game_image']).decode('utf-8')

    return render_template('publisher_new_game.html',
                           is_edit=True,
                           form_action=url_for('edit_game', publisher_id=publisher_id, game_id=game_id),
                           game=game,
                           publisher_id=publisher_id)

def delete_game(publisher_id, game_id):
    organize_game_repository.delete_game(game_id, publisher_id)
    return redirect(url_for('published_games', publisher_id=publisher_id))

