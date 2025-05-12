from model.AccountStatus import AccountStatus
from model.Role import Role  # asumsi Role.py disimpan di model juga

class Account:
    def __init__(self, name='', password='', id=0, role: Role = None, status=AccountStatus.ACTIVE):
        if not isinstance(role, Role):
            raise TypeError("role must be an instance of Role enum.")
        
        self.name = name
        self.password = password
        self.id = id
        self.role = role
        self.status = status

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
        if not isinstance(role, Role):
            raise TypeError("role must be an instance of Role enum.")
        self.role = role
        
    def get_status(self):
        return self.status
    
    def set_status(self, status: AccountStatus):
        self.status = status
