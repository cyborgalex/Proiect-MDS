
#VSCODE pylint throws an error when using SQLAlchemy
#pylint:disable=E1101



from flask import Flask, render_template, redirect,url_for,flash,request
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import *
from math import ceil

app=Flask(__name__)
app.config['SECRET_KEY']="testkey"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db=SQLAlchemy(app)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'



#Function to get the user object from the database so the login manager knows which user to login
@login_manager.user_loader
def load_user(user_id):
    return user.query.filter_by(id=user_id).first()


class paginator:
    def __init__(self, page,per_page,total):
        self.page=page
        self.per_page=per_page
        self.total=total
    
    @property
    def pages(self):
        return int(ceil(float(self.total)/self.per_page))

    @property
    def has_next(self):
        return self.page<self.pages

    @property
    def has_prev(self):
        return self.page>1



@app.route('/index')
@app.route('/')
def index():
    arguments=request.args
    print(request.endpoint)
    if 'page' in arguments:
        page_number=int(arguments['page'])
    else:
        page_number=1

    count=10
    total=post.query.count()
    print(total)
    pag=paginator(page_number,count,total)

    posts=post.query.offset((page_number-1)*count).limit(count).all()
    
    print(posts)
    return render_template('index.html',posts=posts,paginator=pag)

@app.route('/login',methods=['GET','POST'])
def login():
    print(request.endpoint)

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=login_form()
    if form.validate_on_submit():
        new=user.query.filter_by(username=form.username.data).first()
        if new is not None:
            #print(new.password)
            print(check_password_hash(new.password,form.password.data))
            if check_password_hash(new.password,form.password.data):
                login_user(new,remember=form.remember.data)
                return redirect(url_for('index'))
            else:
                flash('Username or password is incorect')
        else:
            flash('Username or password is incorect')
    return render_template('login.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
            return redirect(url_for('index'))

    form=register_form()
    if form.validate_on_submit():
        #ret_query=db.session.query(user.id).filter_by(username=form.username.data).scalar() is not None
        hashed_password=generate_password_hash(form.password.data,method='sha256')
        new=user(username=form.username.data,password=hashed_password,email=form.email.data)
        db.session.add(new)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html',form=form)


@app.route('/post',methods=['GET','POST'])
@login_required
def postingFunction():
    form=post_form()
    if form.validate_on_submit():
        new=post(text=form.post.data,user_id=1)
        db.session.add(new)
        db.session.commit()
    return render_template('post.html',form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
