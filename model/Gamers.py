from model import Acc

class Gamers(Acc):
    def __init__(self, wallet, name, password, id):
        super().__init__(name, password, id)
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