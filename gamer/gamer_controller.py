from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from model.Gamer import Gamer
from model.Cart import Cart
from model.Game import Game
from gamer.repo.gamer_repository import GamerRepository
from controller.db_controller import get_db_connection 
import base64

gamer_bp = Blueprint('gamer', __name__, url_prefix='/gamer')

@gamer_bp.route('/dashboard/<int:gamer_id>')
def gamer_homepage(gamer_id):
    balance = GamerRepository.get_wallet_balance(gamer_id)
    return render_template("home_page.html", gamer_id=gamer_id, wallet_balance=balance)

@gamer_bp.route('/library/<int:gamer_id>')
def gamer_library(gamer_id):
    games = GamerRepository.get_owned_games(gamer_id)
    return render_template('library.html', gamer_id=gamer_id, games=games)

@gamer_bp.route('/store/<int:gamer_id>')
def gamer_store(gamer_id):
    games = GamerRepository.get_unowned_games(gamer_id)
    return render_template('store.html', gamer_id=gamer_id, games=games)

@gamer_bp.route('/buy/<int:gamer_id>/<int:game_id>')
def buy_game(gamer_id, game_id):
    GamerRepository.buy_game(gamer_id, game_id)
    return redirect(url_for('gamer.gamer_library', gamer_id=gamer_id))
