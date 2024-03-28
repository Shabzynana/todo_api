# import datetime
from flask import url_for,flash,request,redirect,Blueprint,abort,jsonify
from todo_api.utils.serializers import user_schema, users_schema
from todo_api import db
from todo_api.models import User, Todo
# from todo_app.users.picture import current_user_id, login_required, check_confirmed


users = Blueprint('users',__name__)


@users.route('/api/register', methods=['GET','POST'])
def register():

    first_name = request.json['first_name']
    last_name = request.json['last_name']
    username = request.json['username']
    email = request.json['email']
    gender = request.json['gender']
    password = request.json['password']

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(first_name,last_name,username,email,gender,hashed_password)
    db.session.add(new_user)
    db.session.commit()

    print(new_user)
    result = user_schema.dump(new_user)
    return jsonify({
        'msg': "User Created",
        'user': result }), 201

@users.route("/api/users", methods=['GET'])    
def all_users():

    users = User.query.all()
    if users:
        result = users_schema.dump(users)
        return {"msg": result}
    return {"msg": "No user yet"}       

@users.route("/api/logout", methods=['POST'])
def logout():
    logout_user()
    return {"msg": "User logout, Successful"}


@users.route('/api/login', methods=['GET','POST'])
def login():

    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()
    if user is None:
        return {"msg": "User with email not found"}, 404

    elif bcrypt.check_password_hash(user.password, password) and user is not None:
        login_user(user)
        return {"msg": "login Successful"}, 200

    elif bcrypt.check_password_hash(user.password, password) is None or user is not None:
        return {"msg": "Incorrect password"}, 400
