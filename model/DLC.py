from model import Item

class DLC(Item):
    def __init__(self, itemID, name, item_type, desc, publisherID, price, status=Item.ItemStatus.NONE):
        super().__init__(itemID, name, item_type, desc, publisherID, price, status)