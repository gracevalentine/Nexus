class ShoppingCart:
    def __init__(self, transaction_id, item_id, description):
        self.transaction_id = transaction_id
        self.item_id = item_id
        self.description = description

    def get_transaction_id(self):
        return self.transaction_id

    def set_transaction_id(self, transaction_id: int):
        self.transaction_id = transaction_id

    def get_item_id(self):
        return self.item_id

    def set_item_id(self, item_id: int):
        self.item_id = item_id

    def get_description(self):
        return self.description

    def set_description(self, description: str):
        self.description = description
