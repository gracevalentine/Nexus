from model.Account import Account

class Gamers(Account):
    def __init__(self, name, password, id):
        super().__init__(name, password, id, role=Account.Role.GAMER)
        self.wallet = 0.0
        self.games = []
        self.dlcs = []

    def get_wallet(self):
        return self.wallet

    def set_wallet(self, wallet):
        self.wallet = wallet

    def get_games(self):
        return self.games

    def set_games(self, games):
        self.games = games

    def get_dlcs(self):
        return self.dlcs

    def set_dlcs(self, dlcs):
        self.dlcs = dlcs
