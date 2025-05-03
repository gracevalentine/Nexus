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
    
    def set_name(self, name: str):
        self.name = name

    def get_password(self):
        return self.password
    
    def set_password(self, password: str):
        self.password = password

    def get_role(self):
        return self.role
    
    def set_role(self, role: Role):
        self.role = role
