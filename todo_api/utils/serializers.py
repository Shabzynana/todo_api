from todo_api import ma
from todo_api.models import User

class User_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = False

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "username", "first_name", "last_name", "gender")

user_schema = UserSchema()
users_schema = UserSchema(many=True)
