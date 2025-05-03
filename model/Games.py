from model import Item, ItemStatus

class Game(Item):
    def __init__(self, itemID, name, item_type, desc, publisherID, price, status= ItemStatus.NONE):
        super().__init__(itemID, name, item_type, desc, publisherID, price, status)
        self.dlcs = []  

    def get_dlcs(self):
        return self.dlcs

    def set_dlcs(self, dlcs):
        self.dlcs = dlcs