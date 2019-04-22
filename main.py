'''
Module DocString-To be added
'''

# SQLAlchemy's database model creates it's atributes at runtime so pylint throws errors
# pylint:disable=E1101


from math import ceil


from flask import Flask, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import DB, User, Post, Tag, LoginForm, PostForm, RegisterForm, ProfileForm

APP = Flask(__name__)
APP.config['SECRET_KEY'] = "testkey"
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
DB.init_app(APP)


tags=['golden retreiver','husky','crossbreed','labrador','dad3addada','dadaddada','dadadadada1','dadadda2da']


# with APP.app_context():
#     DB.create_all()
#     for tag in tags:
#         n=Tag(tag_name=tag)
#         DB.session.add(n)
#     DB.session.commit()

_ADMIN_RANK_ = 1

LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.init_app(APP)
LOGIN_MANAGER.login_view = 'login'

# Function to get the user object from the database so the login manager knows which user to login



@LOGIN_MANAGER.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class Paginator:
    def __init__(self, page, per_page, total):
        self.page = page
        self.per_page = per_page
        self.total = total

    @property
    def pages(self):
        return int(ceil(float(self.total)/self.per_page))

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def has_prev(self):
        return self.page > 1 


@APP.route('/')
@APP.route('/index')
def index():
    arguments = request.args
    if 'page' in arguments:
        page_number = int(arguments['page'])
    else:
        page_number = 1

    count = 10
    total = Post.query.count()
    pag = Paginator(page_number, count, total)

    posts = Post.query.offset((page_number-1)*count).limit(count).all()
    return render_template('index.html', posts=posts, paginator=pag)


@APP.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method=='POST':
        if form.validate_on_submit():
            new = User.query.filter_by(username=form.username.data).first()
            if new is not None:
                if check_password_hash(new.password, form.password.data):
                    login_user(new, remember=form.remember.data)
                    return redirect(url_for('index'))
                else:
                    flash('Username or password is incorect')
            else:
                flash('Username or password is incorect')
    else:
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
    return render_template('login.html', form=form)


@APP.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        query_email = DB.session.query(User.id).filter_by(
            email=form.email.data).scalar() is not None
        query_user = DB.session.query(User.id).filter_by(
            username=form.username.data).scalar() is not None
        if not query_email and not query_user:
            hashed_password = generate_password_hash(
                form.password.data, method='sha256')
            new = User(username=form.username.data,
                       password=hashed_password, email=form.email.data)
            DB.session.add(new)
            DB.session.commit()
            return redirect(url_for('login'))
        else:
            flash('Username or Email already exist')
    return render_template('register.html', form=form)





@APP.route('/post', methods=['GET', 'POST'])
@login_required
def posting_function():
    form = PostForm()
    if request.method=='POST' and form.validate_on_submit():
        new = Post(title=form.title.data,text=form.post.data, user=current_user)
        for split in form.tags.data.split(' '):
            tag=Tag.query.filter_by(tag_name=split).first()
            if tag is not None:
                new.tags.append(tag)
        DB.session.add(new)
        DB.session.commit()
        return redirect(url_for('index'))
    return render_template('post.html', form=form,tags=tags)

def is_admin(user):
    if hasattr(user,'rank') and user.rank==_ADMIN_RANK_:
        return True
    else:
        return False


APP.jinja_env.globals['is_admin']=is_admin

@APP.route('/delete_post', methods=['GET','POST'])
@login_required
def delete_post():
    arguments = request.args
    if 'id' in arguments:
        post_id = int(arguments['id'])
    query_post = Post.query.filter_by(id=post_id).first()
    if query_post.user_id == current_user.id or is_admin(current_user):
        DB.session.delete(query_post)
        DB.session.commit()
    return redirect(url_for('index'))


@APP.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@APP.route('/profile',methods=['POST','GET'])
@login_required
def profile():
    form=ProfileForm()
    if request.method=='POST' and form.validate_on_submit():
        if form.last_name.data:
            current_user.last_name=form.last_name.data
        if form.first_name.data:
            current_user.first_name=form.first_name.data
        if form.phone:
            current_user.phone=form.phone.data
        if form.email:
            current_user.email=form.email.data
        DB.session.commit()
        return redirect(url_for('index'))
    else:
        form.email.data=current_user.email
        form.first_name.data=current_user.first_name
        form.last_name.data=current_user.last_name
        form.phone.data=current_user.phone
    return render_template('profile.html', form=form)
        



if __name__ == '__main__':
    APP.run(debug=True)
