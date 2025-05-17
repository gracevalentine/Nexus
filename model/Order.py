class Order:
    def __init__(self, order_id, gamer_id):
        self._order_id = order_id
        self._gamer_id = gamer_id

    @property
    def order_id(self):
        return self._order_id

    @order_id.setter
    def cart_id(self, value):
        self._order_id = value

    @property
    def gamer_id(self):
        return self._gamer_id

    @gamer_id.setter
    def item_id(self, value):
        self._gamer_id = value

