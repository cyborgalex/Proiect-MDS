from flask_login import UserMixin
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from main import db


#VSCODE pylint throws an error when using SQLAlchemy
#pylint:disable=E1101

class user(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True)
    email = db.Column(db.String(20),unique=True)
    password= db.Column(db.String(80))
    posts=db.relationship('post',backref='user',lazy=True)


class post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    text=db.Column(db.Text(),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    comments=db.relationship('comment',backref='post',lazy=True)

class comment(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    text=db.Column(db.Text(),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    post_id=db.Column(db.Integer,db.ForeignKey('post.id'),nullable=False)

class login_form(FlaskForm):
    username=StringField('username',validators=[InputRequired()])
    password=PasswordField('password',validators=[InputRequired()])
    remember=BooleanField('remember')


class register_form(FlaskForm):
    username=StringField('username',validators=[InputRequired(),Length(min=4,max=20)])
    password=PasswordField('password',validators=[InputRequired(),Length(min=8,max=80)])
    email=StringField('email',validators=[Email(),InputRequired(),Length(min=5,max=80)])


class post_form(FlaskForm):
    post=StringField('post',validators=[InputRequired()])

