# games/route/game_route.py

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from games.controller.game_controller import GameController

game_bp = Blueprint('game', __name__, url_prefix='/games')

@game_bp.route('/')
def index():
    return GameController.index()

@game_bp.route('/<int:game_id>')
def detail(game_id):
    return GameController.detail(game_id)

@game_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        return GameController.add_post(request.form)
    return GameController.add_get()

@game_bp.route('/edit/<int:game_id>', methods=['GET', 'POST'])
def edit(game_id):
    if request.method == 'POST':
        return GameController.edit_post(game_id, request.form)
    return GameController.edit_get(game_id)

@game_bp.route('/delete/<int:game_id>', methods=['POST'])
def delete(game_id):
    return GameController.delete(game_id)

@game_bp.route('/api/list', methods=['GET'])
def api_list():
    # contoh endpoint API JSON
    return jsonify(GameController.api_list())

