'''
Module DocString-To be added
'''
from datetime import datetime
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

# VSCODE pylint throws an error when using SQLAlchemy
# pylint:disable=E1101


class User(UserMixin, DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(20), unique=True)
    email = DB.Column(DB.String(20), unique=True)
    password = DB.Column(DB.String(80))
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
    tag_name = DB.Column(DB.String(20))



class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    remember = BooleanField('remember')


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[
        InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[
        InputRequired(), Length(min=8, max=80)])
    email = StringField('email', validators=[
        Email(), InputRequired(), Length(min=5, max=80)])


class PostForm(FlaskForm):
    post = StringField('post', validators=[InputRequired()])
