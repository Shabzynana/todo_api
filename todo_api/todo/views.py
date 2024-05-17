# import datetime
from flask import url_for,flash,request,redirect,Blueprint,abort,jsonify

from todo_api import db
from todo_api.models import User, Todo
from todo_api.utils.serializers import todo_schema, todos_schema
from todo_api.utils.function import current_user_id, login_required


todos = Blueprint('todos' ,__name__, url_prefix="/api")
 
@todos.route("/create_todo", methods=['POST'])
@login_required
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

@todos.route("/todo/<id>", methods=['GET'])
def todo_id(id):

    todo = Todo.query.get(id)
    if todo:
        return jsonify(
            {"msg": todo_schema.dump(todo)}), 200

    return jsonify({"msg": "No task with such id"})


@todos.route("/update_todo/<id>", methods=['PUT'])
@login_required
def update_todo(id):

    try:
        todo = Todo.query.get_or_404(id)
        if todo.author != current_user_id():
            # Forbidden, No Access
            abort(403)
            return jsonify({"msg": "Not authorized!"})
            # flash('Not authorized', 'danger')
        todo.text = request.json['text']
        todo.date = request.json['date']
        db.session.commit()
        return jsonify({"msg": "task updated"})

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
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    # elif request.method == 'GET':
        # form.text.data = todo.text
        # form.date.data = todo.date

@todos.route("/delete_todo/<id>", methods=['DELETE'])
@login_required
def delete_todo(id):

    try:

        todo = Todo.query.get(id)
        if todo.author != current_user_id():
            abort(403)
            return jsonify(
                {"msg": "Not Authorized!"}), 403
        db.session.delete(todo)
        db.session.commit()
        return jsonify({"msg": "Task Deleted!"})    

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