from flask import render_template, request, redirect, session, url_for, flash
import base64
from organize_game.repo import organize_game_repository
from organize_game.model.GameStatus import GameStatus

def publisher_homepage(publisher_id):
    publisher_id = session.get('publisher_id')
    return render_template('publisher_homepage.html', publisher_id=publisher_id, username=session.get('username', 'Publisher'))

def published_games(publisher_id):
    games = organize_game_repository.get_games_by_publisher(publisher_id)
    games_dict = []

    for game in games:
        game_data = game.to_dict()
        game_data['image_data'] = base64.b64encode(game.image).decode('utf-8') if game.image else None
        game_data['status_label'] = game.status.name
        games_dict.append(game_data)

    return render_template('published_games.html', games=games_dict, publisher_id=publisher_id)

def add_new_game(publisher_id):
    if request.method == 'POST':
        name = request.form['game_name']
        desc = request.form['game_description']
        genre = request.form['game_genre']
        price = request.form['game_price']
        status = 1  # default AVAILABLE status kalau mau pakai enum bisa sesuaikan
        image_file = request.files.get('game_image')
        image_data = image_file.read() if image_file else None

        organize_game_repository.insert_game((name, desc, genre, price, image_data, status, publisher_id))
        flash('Game successfully added!')
        return redirect(url_for('publisher.published_games', publisher_id=publisher_id))

    # GET request (form kosong)
    return render_template(
        'publisher_new_game.html',
        publisher_id=publisher_id,
        is_edit=False,
        form_action=url_for('publisher.add_new_game', publisher_id=publisher_id),
        statuses=[],
        game=None
    )


def edit_game(publisher_id, game_id):
    if request.method == 'POST':
        name = request.form['game_name']
        price = request.form['game_price']
        genre = request.form['game_genre']
        desc = request.form['game_description']
        status = int(request.form['game_status'])
        image_file = request.files.get('game_image')

        if image_file and image_file.filename != '':
            image_data = image_file.read()
            organize_game_repository.update_game(
                game_id, publisher_id,
                (name, price, genre, desc, image_data, status),
                with_image=True
            )
        else:
            organize_game_repository.update_game(
                game_id, publisher_id,
                (name, price, genre, desc, status),
                with_image=False
            )

        flash("Game updated successfully!")
        return redirect(url_for('publisher.published_games', publisher_id=publisher_id))

    game = organize_game_repository.get_game_by_id(game_id, publisher_id)

    if game:
        game_data = game.to_dict()
        if game.image:
            # Asumsi image JPEG, sesuaikan kalau PNG atau lainnya
            game_data['image_data'] = "data:image/jpeg;base64," + base64.b64encode(game.image).decode('utf-8')
        else:
            game_data['image_data'] = None

        return render_template(
            'publisher_new_game.html',
            publisher_id=publisher_id,
            is_edit=True,
            form_action=url_for('publisher.edit_game', publisher_id=publisher_id, game_id=game_id),
            game=game_data,
            statuses=GameStatus
        )

    flash("Game not found.")
    return redirect(url_for('publisher.published_games', publisher_id=publisher_id))


def delete_game(publisher_id, game_id):
    organize_game_repository.delete_game(game_id, publisher_id)
    return redirect(url_for('publisher.published_games', publisher_id=publisher_id))