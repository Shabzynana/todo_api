from flask import url_for, render_template
from flask_mail import Message
from flask_login import current_user


from todo_api import mail
from todo_api.utils.token import get_token

def send_email(user):
    token = get_token(user)
    msg = Message('Email',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.html = render_template('activate_email.html', token=token, _external=True)
    mail.send(msg)



def resend_email(current_user):
    token = get_token(current_user)
    msg = Message('Email',
                  sender='noreply@demo.com',
                  recipients=[current_user.email])
    msg.html = render_template('activate_email.html', token=token, _external=True)
    mail.send(msg)



def send_reset_password(user):
    token = get_token(user)
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.html = render_template('password_reset.html', token=token, _external=True)
    mail.send(msg)
