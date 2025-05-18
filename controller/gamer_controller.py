from flask import Blueprint, render_template
# from flask import Blueprint, render_template, request, redirect, url_for
from model.Admin import Admin
from model.Account import Account
from model.AccountStatus import AccountStatus
from model.Role import Role
from model.Gamer import Gamer
# from controller.db_controller import get_db_connection

gamer_bp = Blueprint('gamer', __name__, url_prefix='/gamer')

# from flask import redirect, url_for

@gamer_bp.route('/dashboard/<int:gamer_id>')
def gamer_homepage(gamer_id):
    return render_template('home_page.html', gamer_id= gamer_id)

@gamer_bp.route('/library/<int:gamer_id>')
def gamer_library(gamer_id):
    return render_template('library.html', gamer_id=gamer_id)

@gamer_bp.route('/storepage/<int:gamer_id>')
def gamer_storepage(gamer_id):
    return render_template('store_category_page.html', gamer_id=gamer_id)