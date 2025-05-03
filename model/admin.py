from model.Account import Account

class Admin(Account):
    def __init__(self, name='', password='', id=0):
        super().__init__(name, password, id, role=Account.Role.ADMIN)
