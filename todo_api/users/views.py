import datetime
from flask import url_for,flash,request,redirect,Blueprint,abort,jsonify,session  #type : ignore
from todo_api.utils.serializers import user_schema, users_schema
from todo_api import db,bcrypt
from todo_api.models import User, Todo
from todo_api.utils.email import send_reset_password, resend_email, send_email
from todo_api.utils.token import verify_token
from todo_api.utils.function import current_user_id, login_required



users = Blueprint('users',__name__, url_prefix="/api", template_folder ="templates/user")



@users.route('/home', methods=['GET'])
def home():

    return jsonify({"message": "i love jesus"})


@users.route('/me')
@login_required
def homeeeee():

    sam = current_user_id()
    result = user_schema.dump(sam)

    return jsonify(
        {"msg": result})


@users.route("/users", methods=['GET'])    
def all_users():

    try:
        users = User.query.all()
        if users:
            result = users_schema.dump(users)
            return jsonify(
                {"msg": result}),200

        return {"msg": "No user yet"} 
    except:
        pass  



@users.route("/users/<int:id>", methods=['GET'])
def user_id(id):

    try:

        user = User.query.get(id)
        if user:
            result = user_schema.dump(user)
            return jsonify(
                {"msg": result}),200

        return jsonify(
                {
                    "error": "failed",
                    "msg": f"No user with such id {id}",
                    })  

    except Exception as error:
        error_message = str(error)  # Convert the error to a string
        print(f"{type(error).__name__}: {error}")
        return (
            jsonify(
                {
                    "error": "failed",
                    "message": error_message,
                }
            ),
            500,
    )            



@users.route("/user/<username>", methods=['GET'])  
def username(username):  

    try:
        user = User.query.filter_by(username=username).first()   
        if user:
            result = user_schema.dump(user)
            return jsonify(
                {"msg": result}),200
        
        return jsonify(
                {
                    "error": "failed",
                    "msg": f"No user with username {username}",
                    })        

    except Exception as error:
        error_message = str(error)  # Convert the error to a string
        print(f"{type(error).__name__}: {error}")
        return (
            jsonify(
                {
                    "error": "failed",
                    "message": error_message,
                }
            ),
            500,
    )                      

         

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


        new_user = User(first_name=first_name,last_name=last_name,username=username,email=email,gender=gender,password=hashed_password,confirmed=False)
        db.session.add(new_user)
        db.session.commit()

        user = User.query.filter_by(email=email).first()
        send_email(user)

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
                }
            ),
            500,
    )              



@users.route('/login', methods=['POST'])
def login():

    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify(
            {"msg": "User with email does not exist"}), 404

    elif bcrypt.check_password_hash(user.password, password) and user is not None:
        session['logged_in'] = True
        session["user_id"] = {"id": user.id}
        
        print(f'login in gee {user.id}')
        return jsonify(
            {"msg": "login Successful"}), 200

    elif bcrypt.check_password_hash(user.password, password) is None or user is not None:
        return jsonify(
            {"msg": "Incorrect password"}), 400


@users.route("/logout", methods=['POST'])
def logout():
    
    session.clear()
    print({"msg": "User logout"})
    return jsonify(
        {
            "msg": "User logout, Successful"
        }
    ),200  


@users.route("/reset_password", methods=['POST'])   
def reset_token():

    email = request.json['email']

    try:

        email_exists = User.query.filter_by(email=email).first()
        if not email_exists:
            return (
                jsonify({"error": "Forbbiden", "message": "Email not found, Please recheck the email!"}),
                403,
            )

        user = User.query.filter_by(email=email).first()
        send_reset_password(user)
        return jsonify (
            {"msg": "An email has been sent with instructions to reset your password"}),200

          
    except Exception as error:
        error_message = str(error)  # Convert the error to a string
        print(f"{type(error).__name__}: {error}")
        return (
            jsonify(
                {
                    "error": "failed",
                    "message": error_message,
                }
            ),
            500,
    )          


@users.route("/reset/<token>", methods=['POST'])   
def reset_password(token):

    password = request.json['password']

    try:

        user = verify_token(token)
        if user is None:
            return jsonify({"msg":"That is an invalid or expired link!"})

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        return jsonify(
            {"msg": "Password Updated, You can now log in!"})

    except Exception as error:
        error_message = str(error)  # Convert the error to a string
        print(f"{type(error).__name__}: {error}")
        return (
            jsonify(
                {
                    "error": "failed",
                    "message": error_message,
                }
            ),
            500,
    )              
       
@users.route('/email/resend', methods=['POST'])
@login_required
def resend():

    resend_email(current_user_id())
    print(f"Email sent to {current_user_id()}")
    return jsonify(
        {"msg": "A new confirmation mail has been sent with instructions to verify your account."}), 200
    

    # try:

    #     resend_email(current_user_id())
    #     return jsonify(
    #         {"msg": "A new confirmation mail has been sent with instructions to verify your account."}), 200
    
    # except Exception as error:
    #     error_message = str(error)  # Convert the error to a string
    #     print(f"{type(error).__name__}: {error}")
    #     return (
    #         jsonify(
    #             {
    #                 "error": "failed",
    #                 "message": error_message,
    #             }
    #         ),
    #         500,
    # )             



@users.route('/confirm/<token>', methods=['POST'])
# @login_required
def confirm_email(token):

    tok = verify_token(token)
    if tok is None:
        return jsonify(
            {"msg": "That is an invalid or expired link"})

    user = User.query.filter_by(id=tok.id).first_or_404()
    if user.confirmed:
        return jsonify(
            {"msg": f"Account already confirmed : {user.username}"}), 200
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        return jsonify (
            {"msg": f"You have confirmed your account. Thanks {user.username}"}), 200

