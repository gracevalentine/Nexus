class Game:
    def __init__(self, game_id, name, description, price, publisher_id):
        self._game_id = game_id
        self._name = name
        self._description = description
        self._price = price
        self._publisher_id = publisher_id

    @property
    def game_id(self):
        return self._game_id

    @game_id.setter
    def game_id(self, value):
        self._game_id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def publisher_id(self):
        return self._publisher_id

    @publisher_id.setter
    def publisher_id(self, value):
        self._publisher_id = value
