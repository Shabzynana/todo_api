from flask import url_for, render_template
from flask_mail import Message
from todo_api import mail


from todo_api.utils.function import current_user_id
from todo_api.utils.token import get_token

def send_email(user):
    token = get_token(user)
    msg = Message('Email',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.html = render_template('users/activate_email.html', token=token, _external=True)
    mail.send(msg)



def resend_email(user):
    token = get_token(user)
    msg = Message('Email',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.html = render_template('users/activate_email.html', token=token, _external=True)
    mail.send(msg)



def send_reset_password(user):
    token = get_token(user)
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.html = render_template('users/password_reset.html', token=token, _external=True)
    mail.send(msg)
