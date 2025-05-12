from model.Account import Account

class Publisher(Account):
    def __init__(self, name='', email = '',password='', id=0):
        super().__init__(name, email, password, id, role=Account.Role.PUBLISHER)
        self.published_games = []
        self.published_dlcs = []

    def get_published_games(self):
        return self.published_games

    def set_published_games(self, game):
        self.published_games = game

    def get_published_dlcs(self):
        return self.published_dlcs

    def set_published_dlcs(self, dlc):
        self.published_dlcs = dlc
