
from model import Acc


class Admin(Acc):
    def __init__(self, name='', password='', id=0):
        super().__init__(name, password, id)
