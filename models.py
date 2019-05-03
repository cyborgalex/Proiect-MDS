

'''
Module DocString-To be added
'''

# SQLAlchemy's database model creates it's atributes at runtime so pylint throws errors
# pylint:disable=E1101


from datetime import datetime
from flask_login import UserMixin
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField,\
     TextAreaField, RadioField, IntegerField
from wtforms.validators import InputRequired, Email, Length, Optional
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()




BONES_USER_POST = DB.Table('bones_user_post',
                           DB.Column('post_id', DB.Integer, DB.ForeignKey('post.id')),
                           DB.Column('user_id', DB.Integer, DB.ForeignKey('user.id')))




class User(UserMixin, DB.Model):
    '''
    Contains informations about a user
    :param int id: Unique id generated for the user upon registration
    :param string email: User's email address
    :param string password: User's password
    :param string first_name: First name
    :param string last_name: Last name
    :param string phone: Phone
    :param posts: Posts made by this user(if not admin will not exist)
    :param int rank: 1-Admin 2-User Default: 2
    '''
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(20), unique=True)
    email = DB.Column(DB.String(20), unique=True)
    password = DB.Column(DB.String(80))
    first_name = DB.Column(DB.String(20))
    last_name = DB.Column(DB.String(20))
    phone = DB.Column(DB.String(20), unique=True)
    posts = DB.relationship('Post', backref='user', lazy=True)
    rank = DB.Column(DB.Integer, DB.ForeignKey('rank.id'), default=2)
    bones = DB.relationship('Post', secondary=BONES_USER_POST)
    comments = DB.relationship('Comment', backref='user', lazy=True)

    def has_liked(self, pid):
        '''
        Return if user has liked a post
        '''
        return Post.query.filter_by(id=pid).first() in self.bones


class Rank(DB.Model):
    '''
    User rank class
    Admin=1
    User=2
    :param int id: Unique id for the rank
    :param str rank_name: Admin/User
    '''
    id = DB.Column(DB.Integer, primary_key=True)
    rank_name = DB.Column(DB.String(20))


POST_TAG = DB.Table('post_tag',
                    DB.Column('post_id', DB.Integer, DB.ForeignKey('post.id')),
                    DB.Column('tag_id', DB.Integer, DB.ForeignKey('tag.id')))



class Post(DB.Model):
    '''
    Post class
    :param int id: Unique id generated for the post
    :param string text: Main body, description of the dog
    :param string title: Dog's name
    :param string gender: Dog's gender
    :param string age: Dog's age
    :param int user_id: User that posted this dog
    :param comments: Comments for this post
    :param tags: Tags selected for this post
    :param date: Post date
    :param images: Images for the post
    '''
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Text(), nullable=False)
    title = DB.Column(DB.String(20), nullable=False)
    gender = DB.Column(DB.String(6))
    age = DB.Column(DB.Integer)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    comments = DB.relationship('Comment', backref='post', lazy=True)
    tags = DB.relationship('Tag', secondary=POST_TAG)
    bones = DB.relationship('User', secondary=BONES_USER_POST)
    date = DB.Column(DB.DateTime, default=datetime.utcnow)
    images = DB.relationship('Image', backref='post', lazy=True)



class Image(DB.Model):
    '''
    Image class
    :param int id: Unique id generated for the image
    :param str name: name+extension
    :param int post_id: Post that has these images
    '''
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String, nullable=False)
    post_id = DB.Column(DB.Integer, DB.ForeignKey('post.id'), nullable=False)


class Comment(DB.Model):
    '''
    Comment class
    :param int id: Unique id generated for the comment
    :param str text: Comment body
    :param user_id: User that posted this
    :param post_id: Post that has this comment
    '''
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Text(), nullable=False)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    post_id = DB.Column(DB.Integer, DB.ForeignKey('post.id'), nullable=False)


class Tag(DB.Model):
    '''
    Tag class
    :param int id: Unique id generated for the tag
    :param str tag_name: Tag name
    '''
    id = DB.Column(DB.Integer, primary_key=True)
    tag_name = DB.Column(DB.String(20), unique=True)



class LoginForm(FlaskForm):
    '''
    Login form
    :param str username: Username
    :param str password: Password
    :param bool remember: Remember user?
    '''
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])
    remember = BooleanField('remember')


class RegisterForm(FlaskForm):
    '''
    Login form
    :param str username: Username
    :param str password: Password
    :param str email: Email
    '''
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    email = StringField('email', validators=[Email(), InputRequired(), Length(min=5, max=80)])


class PostForm(FlaskForm):
    '''
    Post form
    :param str title: Title
    :param str post: Post body
    :param str tags: Tags
    :param upload: Images
    :param gender: Gender
    :param age: Age
    '''
    title = StringField('title', validators=[InputRequired()])
    post = TextAreaField('post', validators=[InputRequired()])
    tags = StringField('tags', validators=[InputRequired()])
    age = IntegerField('age', validators=[Optional()])
    gender = RadioField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')])
    upload = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
        ])

class CommentForm(FlaskForm):
    '''
    Comment Form
    :param str text: Comment body
    '''
    text = TextAreaField('comment', validators=[InputRequired()])

class ProfileForm(FlaskForm):
    '''
    Profile change form
    :param str email: Email
    :param str first_name: First name
    :param str last_name: Last name
    :param str phone: Phone
    '''
    email = StringField('email', validators=[Email(), Length(min=5, max=80), Optional()])
    first_name = StringField('first_name', validators=[Length(min=0, max=20), Optional()])
    last_name = StringField('last_name', validators=[Length(min=0, max=20), Optional()])
    phone = StringField('phone', validators=[Length(min=10, max=10), Optional()])
