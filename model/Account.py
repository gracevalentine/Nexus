from enum import Enum
from model.AccountStatus import AccountStatus


class Role(Enum):
    GAMER = 1
    ADMIN = 2
    PUBLISHER = 3

class Account:
    def __init__(self, name='', email='', password='', id=0, role=Role.GAMER, status=AccountStatus.ACTIVE):
        self.name = name
        self.email = email
        self.password = password
        self.id = id
        self.role = role
        self.status = status

    def get_name(self):
        return self.name
    
    def set_name(self, name: str):
        self.name = name
        
    def get_email(self):
        return self.email
    
    def set_email(self, email: str):
        self.email = email
        
    def get_password(self):
        return self.password
    
    def set_password(self, password: str):
        self.password = password

    def get_role(self):
        return self.role
    
    def set_role(self, role: Role):
        self.role = role
        
    def get_status(self):
        return self.status
    
    def set_status(self, status: AccountStatus):
        self.status = status
