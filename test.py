import unittest
import json
 
from main import APP
from models import DB, User, Post, Comment
 
 

 
class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        with APP.app_context():
            APP.config['TESTING'] = True
            APP.config['WTF_CSRF_ENABLED'] = False
            APP.config['DEBUG'] = False
            APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
            self.APP = APP.test_client()
            DB.init_app(APP)
            DB.drop_all()
            DB.create_all()
        self.assertEqual(APP.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass
 
    # Helper Methods
    
    def register(self, email, password, name):
        return self.APP.post(
            '/register',
            data=dict(username=name,email=email, password=password),
            follow_redirects=True
        )
    
    def login(self, name, password):
        return self.APP.post(
            '/loginn',
            data=dict(username=name, password=password),
            follow_redirects=True
        )

    def get_user_by_name(self,name):
        return User.query.filter_by(username=name).first()

    def logout(self):
        return self.APP.get(
            '/logout',
            follow_redirects=True
        )

    def create_admin(self):
        response = self.register('dada@gmail.com', 'admin123', 'admin')
        with APP.app_context():
            DB.session.query(User).first().rank=1
            DB.session.commit()
        response = self.login('admin', 'admin123')
        self.assertEqual(response.status_code, 200)        

    def post(self, name,desc,age,gender,tags):
        return self.APP.post(
            '/adddog',
            data=dict(title=name,post=desc, age=age, gender=gender,tags=tags),
            follow_redirects=True
        )

    def comment(self, id, text):
        return self.APP.post(
            ('/dog?id=%d'%(id)),
            data=dict(text=text),
            follow_redirects=True
        )
    
    def bone(self,id,action):
         return self.APP.post(('/bone?id=%d'% id),
                    data=json.dumps(dict(id=id, action=action)),
                    follow_redirects=True,
                    content_type='application/json')
    
    # Actual Tests

    def test_main_page(self):
        response = self.APP.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_user_registration_login_logout(self):
        response = self.register('dada@gmail.com', 'test1235', 'test')
        self.assertEqual(response.status_code, 200)
        response = self.login('test', 'test1235')
        self.assertEqual(response.status_code, 200)        
        response=self.logout()
        self.assertIn(b'<title>Home-K9Adopt</title>',response.data)

    def test_logout_without_login(self):
        response=self.logout()
        self.assertIn(b'Please log in to access this page.',response.data)

    def test_register_existing_data(self):
        response = self.register('dada@gmail.com', 'test1235', 'test')
        self.assertEqual(response.status_code, 200)
        response = self.register('dada@gmail.com', 'test1235', 'test')
        self.assertIn(b'Username or Email already exist',response.data)

    def test_admin_user(self):
        self.create_admin()
        response = self.APP.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a dogo',response.data)
        
    def test_valid_posting(self):
        self.create_admin()
        response = self.post("test","testdesc",100,"Male","husky")
        response = self.post("test2","testdesc",100,"Male","husky")
        n=0
        with APP.app_context():
            n=DB.session.query(Post).count()
        self.assertEqual(2,n)

    def test_comments(self):
        self.create_admin()
        self.post("test","testdesc",100,"Male","husky")
        with APP.app_context():
            id=DB.session.query(Post).first().id
        response = self.comment(id,"comentariutest")

        n=0
        with APP.app_context():
            n=DB.session.query(Comment).count()
        self.assertEqual(1,n)

    def test_delete_post(self):
        self.create_admin()
        self.post("test","testdesc",100,"Male","husky")
        with APP.app_context():
            id=DB.session.query(Post).first().id
            countbefore=DB.session.query(Post).count()

        response = self.APP.post(('/delete_post?id=%d'% id), follow_redirects=True)
        with APP.app_context():
            countafter=DB.session.query(Post).count()
        self.assertNotEqual(countbefore,countafter)

    def test_bone(self):
        self.create_admin()
        self.post("test","testdesc",100,"Male","husky")
        with APP.app_context():
            id=DB.session.query(Post).first().id
            likedbefore=DB.session.query(User).first().has_liked(id)
        response = self.bone(id,'like')
        with APP.app_context():
            likedafter=DB.session.query(User).first().has_liked(id)
        self.assertNotEqual(likedbefore,likedafter)

    def test_profile(self):
        self.create_admin()
        self.APP.post(
            '/profile',
            data=dict(last_name="gigel",first_name="adminul",phone="0722222222"),
            follow_redirects=True
        )
        with APP.app_context():
            user=DB.session.query(User).first()
        self.assertEqual(user.last_name,"gigel")
        self.assertEqual(user.first_name,"adminul")
        self.assertEqual(user.phone,"0722222222")
        

                
if __name__ == "__main__":
    unittest.main()