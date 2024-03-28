from todo_api import db
import datetime

class User(db.Model): # type: ignore

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    profile_image = db.Column(db.String(64),nullable=False,default='default_profile.png')
    email = db.Column(db.String(64),unique=True,index=True)
    first_name = db.Column(db.String(64),unique=False,index=True)
    last_name = db.Column(db.String(64),unique=False,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    gender = db.Column(db.String(10))
    password = db.Column(db.String(128))
    registered_on = db.Column(db.DateTime,nullable=False,default=datetime.datetime.now())
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    todos = db.relationship('Todo',backref='author',lazy=True,cascade='all, delete-orphan')

    def __init__(self,email,first_name,last_name,username,gender,password,confirmed,confirmed_on=None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.gender = gender
        self.password = password
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on


    def __repr__(self):
        return f" Username {self.username}"
    
class Todo(db.Model):   # type: ignore

    __tablename__ = 'todos'

    id = db.Column(db.Integer,primary_key = True)
    text = db.Column(db.Text,nullable=False)
    date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.String(64),db.ForeignKey('users.username',onupdate="CASCADE"),nullable=False)


    def __init__(self,text,user_id,date):
        self.text = text
        self.user_id = user_id
        self.date = date

    def __repr__(self):
        return f"Post Id: {self.id}"
