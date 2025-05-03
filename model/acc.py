from enum import Enum

class Role(Enum):
    GAMER = 1
    ADMIN = 2
    PUBLISHER = 3

class Account:
    def __init__(self, name='', password='', id=0, role=Role.GAMER):
        self.name = name
        self.password = password
        self.id = id
        self.role = role

    def get_name(self):
        return self.name

    def get_password(self):
        return self.password

    def get_role(self):
        return self.role
