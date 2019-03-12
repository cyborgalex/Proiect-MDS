from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime

db = SQLAlchemy()

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
    #date=db.Column(db.DateTime,default=datetime.datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    comments=db.relationship('comment',backref='post',lazy=False)
    #images=db.relationship('image',backref='post',lazy=True)


class comment(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    text=db.Column(db.Text(),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    post_id=db.Column(db.Integer,db.ForeignKey('post.id'),nullable=False)

#class image(db.Model):
    #id=db.Column(db.Integer,primary_key=True)
    #path=db.Column(db.String(100),nullable=False)
    #post_id=db.Column(db.Integer,db.ForeignKey('post.id'),nullabe=False)


