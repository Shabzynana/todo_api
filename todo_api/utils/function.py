import os
import secrets
from flask import url_for, flash, current_app, redirect, session, jsonify
from functools import wraps
from todo_api.models import User



def current_user_id():
    if 'user_id' in session:
        id = session['user_id']['id']
        user = User.query.filter_by(id=id).first()
        if user:
            return user
    return (
        {"msg": "NO USER, Please Login In"}), 400     


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user_id().confirmed is False:
            return redirect(url_for('users.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function


# def user_check(func):
#     @wraps(func)
#     def decorated_function(username, *args, **kwargs):
#         user = User.query.filter_by(username=username).first()
#         if current_user != user:
#             flash('User not authorized', 'danger')
#             return redirect(url_for('users.all_user_todos', username=current_user.username))
#         return func(username, *args, **kwargs)

#     return decorated_function


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return jsonify({"msg": "Please Log In!"})
        return func(*args, **kwargs)
        
    return inner
   