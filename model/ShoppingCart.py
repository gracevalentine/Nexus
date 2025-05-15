class ShoppingCart:
    def __init__(self, cart_id, game_id, description):
        self.cart_id = cart_id
        self.item_id = game_id
        self.description = description

    def get_cart_id(self):
        return self.cart_id
    
    def set_cart_id(self, cart_id: int):
        self.cart_id = cart_id
        
    def get_item_id(self):
        return self.game_id

    def set_item_id(self, game_id: int):
        self.game_id = game_id

    def get_description(self):
        return self.description

    def set_description(self, description: str):
        self.description = description
