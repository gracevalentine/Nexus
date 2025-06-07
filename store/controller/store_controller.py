from flask import render_template, request, jsonify, flash, redirect, session, url_for
from store.repo import store_repository
from order.repo import order_repository
import base64

def storepage(gamer_id):
    if 'username' not in session:
        return redirect(url_for('auth.login_controller'))

    raw_games = store_repository.get_all_games()

    games = []
    for item in raw_games:
        game = item["game"]
        image_blob = item["image_blob"]
        publisher_name = item["publisher_name"]

        image_data = base64.b64encode(image_blob).decode('utf-8') if image_blob else None
        image_url = f"data:image/jpeg;base64,{image_data}" if image_data else "/static/asset/default.jpg"

        games.append({
            "id": game.game_id,
            "name": game.name,
            "description": game.description,
            "genre": game.genre,
            "price": game.price,
            "publisher": publisher_name,  # bukan dari game
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

def add_review(gamer_id, game_id):
    data = request.get_json()
    review_text = data.get("review", "").strip()

    if not review_text:
        return jsonify({"status": "error", "message": "Review kosong!"})

    try:
        store_repository.add_review(review_text, gamer_id, game_id)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def get_reviews(game_id):
    rows = store_repository.get_reviews(game_id)
    result = result = []
    for r in rows:
        result.append({
            "review_id": r.review_id,
            "review_text": r.review_text,
            "reviewer": r.reviewer,
            "game_name": r.game.name,
            "date": r.date.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(reviews=result)
