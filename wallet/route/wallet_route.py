from flask import Blueprint, redirect, render_template, session, url_for
from wallet.controller import wallet_controller


wallet_bp = Blueprint(
    'wallet',
    __name__,
    template_folder='../view',
    static_folder='../view',
    static_url_path='/wallet_static'
)

wallet_bp.route('/wallet/<int:gamer_id>')(wallet_controller.walletpage)
wallet_bp.route('/wallet/topup/<int:gamer_id>', methods=['GET', 'POST'])(wallet_controller.topup_wallet)
