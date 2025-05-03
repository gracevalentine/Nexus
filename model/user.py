from config.redis_config import r
import json

class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def save(self):
        r.set(f"user:{self.id}", json.dumps({'id': self.id, 'name': self.name}))

    @staticmethod
    def get_by_id(user_id):
        data = r.get(f"user:{user_id}")
        if data:
            user_data = json.loads(data)
            return User(user_data['id'], user_data['name'])
        return None
