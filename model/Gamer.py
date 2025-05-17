from model.Account import Account

class Gamer(Account):
    def __init__(self, name, password, id):
        super().__init__(name, '', password, id, role=Account.Role.GAMER)
        self._wallet = 0.0
        self._games = []

    @property
    def wallet(self):
        return self._wallet

    @wallet.setter
    def wallet(self, value):
        self._wallet = value

    @property
    def games(self):
        return self._games

    @games.setter
    def games(self, value):
        self._games = value
