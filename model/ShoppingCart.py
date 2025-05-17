class ShoppingCart:
    def __init__(self, cart_id, game_id, description):
        self._cart_id = cart_id
        self._item_id = game_id
        self._description = description

    @property
    def cart_id(self):
        return self._cart_id

    @cart_id.setter
    def cart_id(self, value):
        self._cart_id = value

    @property
    def item_id(self):
        return self._item_id

    @item_id.setter
    def item_id(self, value):
        self._item_id = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value
