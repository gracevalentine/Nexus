from datetime import datetime
from model.Account import Account

class Publisher(Account):
    def __init__(self, name='', email='', password='', id=0, historyPublishedGames: datetime = None):
        super().__init__(name, email, password, id, role=Account.Role.PUBLISHER)
        self._published_games = []
        self._history_published_games = historyPublishedGames or datetime.now()

    @property
    def published_games(self):
        return self._published_games

    @published_games.setter
    def published_games(self, value):
        self._published_games = value
        
    @property
    def history_published_games(self):
        return self._history_published_games
    
    @history_published_games.setter
    def history_published_games(self, value):
        if not isinstance(value, datetime):
            raise TypeError("history_published_games must be a datetime object")
        self._history_published_games = value
