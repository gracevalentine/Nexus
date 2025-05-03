class item:
    def __init__(self, itemID: int,name: str, type: str, desc: str, publisherID: int, price: float):
        self.itemID = itemID
        self.name = name
        self.type = type
        self.desc = desc
        self.publisherID = publisherID
        self.price = price
        
    def get_itemID(self):
        return self.itemID
    
    def set_itemID(self, itemID: int):
        self.itemID = itemID
        
    def get_name(self):
        return self.name
    
    def set_name(self, name: str):
        self.name = name    
        
    def get_type(self):
        return self.type    
    
    def set_type(self, type: str):
        self.type = type
        
    def get_desc(self):
        return self.desc
    
    def set_desc(self, desc: str):
        self.desc = desc
        
    def get_publisherID(self):
        return self.publisherID
    
    def set_publisherID(self, publisherID: int):
        self.publisherID = publisherID
        
    def get_price(self):
        return self.price
    
    def set_price(self, price: float):
        self.price = price
    
    