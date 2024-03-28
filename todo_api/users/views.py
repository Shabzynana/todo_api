import datetime
from flask import url_for,flash,request,redirect,Blueprint,abort,jsonify
from todo_api.users.serializers import user_schema, users_schema

from todo_api import db
from todo_api.models import User, Todo
# from todo_app.users.picture import current_user_id, login_required, check_confirmed


users = Blueprint('users',__name__)

@users.route('/api/register', methods=['POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data,username=form.username.data,first_name=form.first_name.data,last_name=form.last_name.data,gender=form.gender.data,password=hashed_password,confirmed=False)

        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(email=form.email.data).first()
        send_email(user)
        flash('Registration Completed', 'info')
        # flash('An email has been sent with instructions to verify your account.', 'info')
        return redirect(url_for('users.login'))

    return render_template('register.html',form=form)