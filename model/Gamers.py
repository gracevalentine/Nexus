from model import Account

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
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "role": "GAMER",
            "wallet": self.wallet,
            "games": self.games,
            "dlcs": self.dlcs
        }

    @staticmethod
    def from_dict(data):
        gamer = Gamers(data["name"], data["password"], data["id"])
        gamer.set_wallet(data.get("wallet", 0.0))
        gamer.set_games(data.get("games", []))
        gamer.set_dlcs(data.get("dlcs", []))
        return gamer