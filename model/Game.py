class Game:
    def __init__(self, game_id, name, description, price, publisher_id):
        self.game_id = game_id
        self.name = name
        self.description = description
        self.price = price
        self.publisher_id = publisher_id
        
    def get_game_id(self):
        return self.game_id
    
    def set_game_id(self, game_id): 
        self.game_id = game_id
        
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
        
    def get_description(self):
        return self.description
    def set_description(self, description):
        self.description = description
    def get_price(self):
        return self.price
    def set_price(self, price):
        self.price = price
    def get_publisher_id(self):
        return self.publisher_id
    def set_publisher_id(self, publisher_id):
        self.publisher_id = publisher_id
        
