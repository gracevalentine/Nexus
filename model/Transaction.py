from datetime import datetime

class Transaction:
    def __init__(self, transaction_id=0, gamer_id=0, date=None):
        if date is None:
            date = datetime.now()
        self._transaction_id = transaction_id
        self._gamer_id = gamer_id
        self._date = date

    @property
    def transaction_id(self):
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, value):
        self._transaction_id = value

    @property
    def gamer_id(self):
        return self._gamer_id

    @gamer_id.setter
    def gamer_id(self, value):
        self._gamer_id = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value
