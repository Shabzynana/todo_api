# import datetime
from flask import url_for,flash,request,redirect,Blueprint,abort

from todo_api import db
from todo_api.models import User, Todo
# from todo_app.users.picture import current_user_id, login_required, check_confirmed


todos = Blueprint('todos',__name__)