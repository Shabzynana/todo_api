from todo_api import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "username", "first_name", "last_name", "gender")

user_schema = UserSchema()
users_schema = UserSchema(many=True)
