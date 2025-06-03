from model.Game import Game
from datetime import datetime

class Review:
    def __init__(self, review_id: int, review_text: str, game: Game = None, reviewer=None, date: datetime = None):
        if game is not None and not isinstance(game, Game):
            raise TypeError("game must be an instance of Game")
        self._review_id = review_id
        self._review_text = review_text
        self._game = game
        self._reviewer = reviewer
        self._date = date or datetime.now()  # default: sekarang

    @property
    def review_id(self):
        return self._review_id

    @review_id.setter
    def review_id(self, value):
        self._review_id = value

    @property
    def review_text(self):
        return self._review_text

    @review_text.setter
    def review_text(self, value):
        self._review_text = value

    @property
    def game(self):
        return self._game

    @game.setter
    def game(self, value):
        if not isinstance(value, Game):
            raise TypeError("game must be an instance of Game")
        self._game = value

    @property
    def reviewer(self):
        return self._reviewer

    @reviewer.setter
    def reviewer(self, value):
        self._reviewer = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if not isinstance(value, datetime):
            raise TypeError("date must be a datetime object")
        self._date = value
