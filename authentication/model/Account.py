from authentication.model.AccountStatus import AccountStatus
from authentication.model.Role import Role

class Account:
    def __init__(self, name='', email='', password='', id=0, role: Role = None, status=AccountStatus.NOT_BANNED):
        if not isinstance(role, Role):
            raise TypeError("role must be an instance of Role enum.")
        self._name = name
        self._email = email 
        self._password = password
        self._id = id
        self._role = role
        self._status = status

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @property
    def id(self):
        return self._id

    @property
    def role(self):
        return self._role

    @property
    def status(self):
        return self._status

    @name.setter
    def name(self, value):
        self._name = value

    @email.setter
    def email(self, value):
        self._email = value

    @password.setter
    def password(self, value):
        self._password = value

    @id.setter
    def id(self, value):
        self._id = value

    @role.setter
    def role(self, value: Role):
        if not isinstance(value, Role):
            raise TypeError("role must be an instance of Role enum.")
        self._role = value

    @status.setter
    def status(self, value: AccountStatus):
        self._status = value