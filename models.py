

'''
Module DocString-To be added
'''

# SQLAlchemy's database model creates it's atributes at runtime so pylint throws errors
# pylint:disable=E1101


from datetime import datetime
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,TextAreaField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, Email, Length,Optional
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()




class User(UserMixin, DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(20), unique=True)
    email = DB.Column(DB.String(20), unique=True)
    password = DB.Column(DB.String(80))
    first_name = DB.Column(DB.String(20))
    last_name = DB.Column(DB.String(20))
    phone = DB.Column(DB.String(20), unique=True)
    posts = DB.relationship('Post', backref='user', lazy=True)
    rank = DB.Column(DB.Integer, DB.ForeignKey('rank.id'), default=2)


class Rank(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    rank_name = DB.Column(DB.String(20))



POST_TAG = DB.Table('post_tag',
                    DB.Column('post_id', DB.Integer, DB.ForeignKey('post.id')),
                    DB.Column('tag_id', DB.Integer, DB.ForeignKey('tag.id'))
                    )


class Post(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Text(), nullable=False)
    title = DB.Column(DB.Text(), nullable=False)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    comments = DB.relationship('Comment', backref='post', lazy=True)
    tags = DB.relationship('Tag', secondary=POST_TAG)
    date = DB.Column(DB.DateTime, default=datetime.utcnow)



class Comment(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Text(), nullable=False)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    post_id = DB.Column(DB.Integer, DB.ForeignKey('post.id'), nullable=False)


class Tag(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    tag_name = DB.Column(DB.String(20), unique=True)



class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    remember = BooleanField('remember')


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    email = StringField('email', validators=[Email(), InputRequired(), Length(min=5, max=80)])


class PostForm(FlaskForm):
    title = StringField('title', validators=[InputRequired()])
    post = TextAreaField('post', validators=[InputRequired()])
    tags=StringField('tags', validators=[InputRequired()])


class ProfileForm(FlaskForm):
    email = StringField('email', validators=[Email(), Length(min=5, max=80), Optional()])
    first_name = StringField('first_name', validators=[Length(min=0, max=20), Optional()])
    last_name = StringField('last_name', validators=[Length(min=0, max=20), Optional()])
    phone = StringField('phone',validators=[Length(min=10,max=10),Optional()])
