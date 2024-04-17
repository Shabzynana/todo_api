from todo_api import ma
from todo_api.models import User

from marshmallow import Schema, fields

# from todo_api.ma import Schema, fields 
from pydantic import BaseModel, EmailStr, constr, validator


# class User_Schema(BaseModel):
#     email: EmailStr
#     username: constr
#     first_name: constr
#     last_name: constr
#     # gender: constr
#     # name: constr(regex=r'^[a-zA-Z0-9_]+$',to_lower=True, min_length=2, max_length=64)
#     password: constr(min_length=8, max_length=64)


# class User_Schema(ma.SQLAlchemySchema):
#     class Meta:
#         model = User

#     username = ma.auto_field()
#     email = ma.auto_field()
#     first_name = ma.auto_field()
#     last_name = ma.auto_field()
#     gender = ma.auto_field()
#     password = ma.auto_field()



# class User_Schema(Schema):
#     username = fields.Str()
#     email = fields.Email()
#     first_name = fields.Str()
#     last_name = fields.Str()
#     gender = fields.Str()
#     password = fields.Str()


class User_Schema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = False

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "username", "first_name", "last_name", "gender")

user_schema = UserSchema()
users_schema = UserSchema(many=True)
