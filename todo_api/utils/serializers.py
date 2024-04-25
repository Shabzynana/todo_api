from todo_api import ma
from todo_api.models import User



class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "username", "first_name", "last_name", "gender")

user_schema = UserSchema()
users_schema = UserSchema(many=True)



class TodoSchema(ma.Schema):
    class Meta:
        fields = ("id", "text", "date", "user_id")

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)
