from model.ItemStatus import ItemStatus

class Item:
    def __init__(self, itemID: int, name: str, item_type: str, desc: str,
                 publisherID: int, price: float, status: ItemStatus = ItemStatus.NONE):
        
        if not isinstance(status, ItemStatus):
            raise TypeError("status must be an instance of ItemStatus enum.")

        self.itemID = itemID
        self.name = name
        self.item_type = item_type
        self.desc = desc
        self.publisherID = publisherID
        self.price = price
        self.status = status

    def get_itemID(self):
        return self.itemID
    
    def set_itemID(self, itemID: int):
        self.itemID = itemID

    def get_name(self):
        return self.name
    
    def set_name(self, name: str):
        self.name = name

    def get_type(self):
        return self.item_type
    
    def set_type(self, item_type: str):
        self.item_type = item_type

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

    def get_status(self):
        return self.status
    
    def set_status(self, status: ItemStatus):
        if not isinstance(status, ItemStatus):
            raise TypeError("status must be an instance of ItemStatus enum.")
        self.status = status
