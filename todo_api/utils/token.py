from time import time
import jwt
from todo_api.config import App_Config
from todo_api.models import User


def get_token(self, expires_in=180):
    return jwt.encode(
        {'user_id': self.id, 'exp': time() + expires_in}, App_Config.SECRET_KEY, algorithm='HS256')


def verify_token(token):
    try:
        user_id = jwt.decode(token, App_Config.SECRET_KEY, algorithms=['HS256'])['user_id']
    except:
        return None
    return User.query.get(user_id)
