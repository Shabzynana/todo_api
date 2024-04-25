# import datetime
from flask import url_for,flash,request,redirect,Blueprint,abort,jsonify

from todo_api import db
from todo_api.models import User, Todo
from todo_api.utils.serializers import todo_schema, todos_schema
from todo_api.utils.function import current_user_id, login_required


todos = Blueprint('todos' ,__name__, url_prefix="/api")
 
@todos.route("/create_todo", methods=['POST'])
def create_todo():

    try:

        text = request.json['text']
        date = request.json['date']

        todo = Todo(text=text, date=date, user_id=current_user_id().username)
        db.session.add(todo)
        db.session.commit()

        return jsonify({"msg": "task created!"})

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

@todos.route("/all_todo", methods=['GET'])
def all_todos():

    try:

        todo = Todo.query.all()
        return jsonify(
            {"msg": todos_schema.dump(todo)})

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

@todos.route("/todo/<int>", methods=['GET'])
def todo_id(int):

    todo = Todo.query.get(id)
    if todo:
        return jsonify({"msg": todo_schema.dump(todo)})

    return jsonify({"msg": "No task with such id"})
    

