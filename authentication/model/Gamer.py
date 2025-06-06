from authentication.model.Account import Account
from authentication.model.Role import Role
from authentication.model.AccountStatus import AccountStatus

class Gamer(Account):
    def __init__(self, name, email, password, id, role=Role.GAMER, status=AccountStatus.NOT_BANNED, wallet=0.0):
        super().__init__(name, email, password, id, role=role, status=status)
        self._wallet = wallet
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

    @staticmethod
    def from_db(account_id, name, email, password, role, status, wallet):
        return Gamer(
            name=name,
            email=email,
            password=password,
            id=account_id,
            role=role,
            status=status,
            wallet=wallet
        )
