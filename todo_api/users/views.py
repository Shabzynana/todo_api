# import datetime
from flask import url_for,flash,request,redirect,Blueprint,abort,jsonify,session  #type : ignore
from todo_api.utils.serializers import user_schema, users_schema,User_Schema
from todo_api import db,bcrypt
from todo_api.models import User, Todo
# from todo_app.users.picture import current_user_id, login_required, check_confirmed


users = Blueprint('users',__name__,url_prefix="/api")



@users.route('/home', methods=['GET'])
def home():

    return jsonify({"message": "i love jesus"})

@users.route("/users", methods=['GET'])    
def all_users():

    try:
        users = User.query.all()
        if users:
            result = users_schema.dump(users)
            return {"msg": result}
        return {"msg": "No user yet"} 
    except:
        pass     


         


@users.route('/register', methods=['POST'])
def register():

    # data = request.get_json() if request.get_json() != None else request.form

    # try:
    #     data = User_Schema(**data)

    #     email_exists = User.query.filter_by(email=data.email).first()
    #     if email_exists:
    #         return (
    #             jsonify({"error": "Forbbiden", "message": "Email already exists!"}),
    #             403,
    #         )

    #     hashed_password = bcrypt.generate_password_hash(data.password).decode("utf-8")

    #     new_user = User(email=data.email, first_name=data.first_name, last_name=data.last_name, username=data.username, gender=data.gender, password=hashed_password)
    #     db.session.add(new_user)
    #     db.sesssion.commit()

    #     return (
    #         jsonify(
    #             {
    #                 "message": "User Created Succesfully",
    #                 "data": user_schema.dump(new_user),
    #             }
    #         ),
    #         201,
    #     )
    # except:
    #     return jsonify({"message":"failed"})    
    # except Exception as error:
    #     error_message = str(error)  # Convert the error to a string
    #     print(f"{type(error).__name__}: {error}")
    #     return (
    #         jsonify(
    #             {
    #                 "error": "failed",
    #                 "message": error_message
    #                 # "message": "Internal Error: User not created",
    #             }
    #         ),
    #         500,
    #     )
    

    try:

        first_name = request.json['first_name']
        last_name = request.json['last_name']
        username = request.json['username']
        email = request.json['email']
        gender = request.json['gender']
        password = request.json['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            return (
                jsonify({"error": "Forbbiden", "message": "Email already exists!"}),
                403,
            )


        new_user = User(first_name=first_name, last_name=last_name,username=username,email=email,gender=gender,password=hashed_password,confirmed=False)
        db.session.add(new_user)
        db.session.commit()

        print(new_user)
        result = user_schema.dump(new_user)
        return jsonify({
            'msg': "User Created",
            'user': result }), 201


    except Exception as error:
        error_message = str(error)  # Convert the error to a string
        print(f"{type(error).__name__}: {error}")
        return (
            jsonify(
                {
                    "error": "failed",
                    "message": error_message,
                    "message": "Internal Error: User not created",
                }
            ),
            500,
    )              



# @users.route("/api/logout", methods=['POST'])
# def logout():
#     logout_user()
#     return {"msg": "User logout, Successful"}


@users.route('/login', methods=['POST'])
def login():

    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify(
            {"msg": "User with email not found"}), 404

    elif bcrypt.check_password_hash(user.password, password) and user is not None:
        session['logged_in'] = True
        session["user_id"] = {"id": user.id}
        
        print(f'login in gee {user.id}')
        return jsonify(
            {"msg": "login Successful"}), 200

    elif bcrypt.check_password_hash(user.password, password) is None or user is not None:
        return jsonify(
            {"msg": "Incorrect password"}), 400