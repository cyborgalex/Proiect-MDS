
cybBranch
#VSCODE pylint throws an error when using SQLAlchemy
#pylint:disable=E1101

from flask import Flask, render_template, redirect, url_for,flash
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import random



app=Flask(__name__)
app.config['SECRET_KEY']="testkey"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db=SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

class user(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True)
    email = db.Column(db.String(20),unique=True)
    password= db.Column(db.String(80))
class login_form(FlaskForm):
    username=StringField('username',validators=[InputRequired(),Length(min=4,max=20)])
    password=PasswordField('password',validators=[InputRequired(),Length(min=8,max=80)])
    



class register_form(FlaskForm):
    username=StringField('username',validators=[InputRequired(),Length(min=4,max=20)])
    password=PasswordField('password',validators=[InputRequired(),Length(min=8,max=80)])
    email=StringField('email',validators=[Email(),InputRequired(),Length(min=5,max=80)])




@app.route('/')
def index():

    return render_template('index.html',form=login_form())

@app.route('/login',methods=['GET','POST'])
def login():
    form=login_form()
    if form.validate_on_submit():
        new=user.query.filter_by(username=form.username.data).first()
        if new:
            return new.username
    return render_template('index.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form=register_form()
    if form.validate_on_submit():
        #ret_query=db.session.query(user.id).filter_by(username=form.username.data).scalar() is not None
        hashed_password=generate_password_hash(form.password.data,method='sha256')
        new=user(username=form.username.data,password=hashed_password,email=form.email.data)
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html',form=form)



if __name__ == '__main__':
    app.run(debug=True)

master
