from datetime import datetime

class Transaction:
    def __init__(self, transaction_id=0, user_id=0, date=None, shopping_cart=None):
        if date is None:
            date = datetime.now()  # Set default to current timestamp if not provided
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.date = date
        self.shopping_cart = shopping_cart

    def get_transaction_id(self):
        return self.transaction_id

    def set_transaction_id(self, transaction_id: int):
        self.transaction_id = transaction_id

    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id: int):
        self.user_id = user_id

    def get_date(self):
        return self.date

    def set_date(self, date: datetime):
        self.date = date

    def get_shopping_cart(self):
        return self.shopping_cart

    def set_shopping_cart(self, shopping_cart):
        self.shopping_cart = shopping_cart
