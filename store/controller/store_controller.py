from flask import render_template, request, jsonify, flash, redirect, session, url_for
from store.repo import store_repository
import base64

def storepage(gamer_id):
    if 'username' not in session:
        return redirect(url_for('auth.login_controller'))
    
    rows = store_repository.get_all_games()  # pake method baru ambil semua game

    games = []
    for game_id, name, description, price, image_blob, publisher_name in rows:
        image_data = base64.b64encode(image_blob).decode('utf-8') if image_blob else None
        image_url = f"data:image/jpeg;base64,{image_data}" if image_data else "/static/asset/default.jpg"

        games.append({
            "id": game_id,
            "name": name,
            # "genre": genre,
            "description": description,
            "price": price,
            "publisher": publisher_name,
            "image": image_url
        })

    return render_template('gamer_stores.html', gamer_id=gamer_id, games=games)

def genre_detail(genre, gamer_id):
    rows = store_repository.get_games_by_genre(genre)

    games = []
    for game_id, name, description, price, image_blob, publisher in rows:
        image_data = base64.b64encode(image_blob).decode('utf-8') if image_blob else None
        image_url = f"data:image/jpeg;base64,{image_data}" if image_data else "/static/asset/default.jpg"

        games.append({
            "id": game_id,
            "name": name,
            "description": description,
            "price": price,
            "publisher": publisher,
            "image": image_url
        })

    return render_template('gamer_stores.html', genre=genre, gamer_id=gamer_id, games=games)
