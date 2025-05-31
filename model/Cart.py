class Cart:
    def __init__(self, gamer_id=None, game_id=None, date_added=None):
        self._gamer_id = gamer_id
        self._game_id = game_id
        self._date_added = date_added

    # === Getter ===
    def get_gamer_id(self):
        return self._gamer_id

    def get_game_id(self):
        return self._game_id

    def get_date_added(self):
        return self._date_added

    # === Setter ===
    def set_gamer_id(self, gamer_id):
        self._gamer_id = gamer_id

    def set_game_id(self, game_id):
        self._game_id = game_id

    def set_date_added(self, date_added):
        self._date_added = date_added