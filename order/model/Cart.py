class Cart:
    def __init__(self, gamer_id=None, game_id=None, date_added=None):
        self._gamer_id = gamer_id
        self._game_id = game_id
        self._date_added = date_added

    @property
    def gamer_id(self):
        return self._gamer_id

    @gamer_id.setter
    def gamer_id(self, value):
        self._gamer_id = value

    @property
    def game_id(self):
        return self._game_id

    @game_id.setter
    def game_id(self, value):
        self._game_id = value

    @property
    def date_added(self):
        return self._date_added

    @date_added.setter
    def date_added(self, value):
        self._date_added = value
