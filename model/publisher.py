from model.Account import Account

class Publisher(Account):
    def __init__(self, name='', email='', password='', id=0):
        super().__init__(name, email, password, id, role=Account.Role.PUBLISHER)
        self._published_games = []

    @property
    def published_games(self):
        return self._published_games

    @published_games.setter
    def published_games(self, value):
        self._published_games = value
