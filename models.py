from database import db

class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    @staticmethod
    def get_by_credentials(username, password):
        user_data = db.get_user_by_credentials(username, password)
        if user_data:
            return User(user_data['id'], user_data['name'])
        return None
    
    @staticmethod
    def get_by_username(username):
        return db.get_user_by_username(username)
    
    @staticmethod
    def create(username, password):
        return db.create_user(username, password)
    
    @staticmethod
    def get_by_id(user_id):
        user_data = db.get_user_by_id(user_id)
        if user_data:
            return User(user_data['id'], user_data['name'])
        return None