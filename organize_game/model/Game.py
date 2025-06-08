from organize_game.model.GameStatus import GameStatus

class Game:
    def __init__(self, game_id, name, description, genre, price, publisher_id, status, image=None):
        self._game_id = game_id
        self._name = name
        self._description = description
        self._genre = genre
        self._price = price
        self._publisher_id = publisher_id
        # safe convert status ke GameStatus enum, kalau gagal default ke AVAILABLE
        try:
            if isinstance(status, GameStatus):
                self._status = status
            elif isinstance(status, int):
                self._status = GameStatus(status)
            elif isinstance(status, str):
                self._status = GameStatus[status]
            else:
                self._status = GameStatus.AVAILABLE
        except (ValueError, KeyError):
            self._status = GameStatus.AVAILABLE
        self._image = image

    @property
    def game_id(self): return self._game_id
    @property
    def name(self): return self._name
    @property
    def description(self): return self._description
    @property
    def genre(self): return self._genre
    @property
    def price(self): return self._price
    @property
    def publisher_id(self): return self._publisher_id
    @property
    def status(self): return self._status
    @property
    def image(self): return self._image

    def to_dict(self):
        return {
            "game_id": self._game_id,
            "game_name": self._name,
            "game_desc": self._description,
            "game_genre": self._genre,
            "game_price": self._price,
            "publisher_id": self._publisher_id,
            "game_status": self._status.value,
            "game_image": self._image
        }