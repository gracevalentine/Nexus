from flask import Blueprint, render_template
from controller.db_controller import get_db_connection 

publisher_bp = Blueprint('publisher', __name__, url_prefix='/publisher')

@publisher_bp.route('/dashboard/<int:publisher_id>')
def publisher_homepage(publisher_id):
    return render_template('publisher_homepage.html', publisher_id=publisher_id)

@publisher_bp.route('/publishedgames/<int:publisher_id>')
def published_games(publisher_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('SELECT * FROM game WHERE publisher_id = %s', (publisher_id,))
    games = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('published_games.html', games=games, publisher_id=publisher_id)
