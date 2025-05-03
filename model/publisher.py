from model import Account

class Publisher(Account):
    def __init__(self, name, password, id):
        super().__init__(name, password, id)
        self.published_games = []
        self.published_dlcs = []

    def get_published_games(self):
        return self.published_games

    def set_published_games(self, games):
        self.published_games = games

    def get_published_dlcs(self):
        return self.published_dlcs

    def set_published_dlcs(self, dlcs):
        self.published_dlcs = dlcs
