from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

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

