from app import app
from models import User, db, Post
from unittest import TestCase
from flask import session
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class AppTestCase(TestCase):
    def test_users_page(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_users_form(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<label for="first-name">First Name:</label>', html)

    
class UserModelTestCase(TestCase):

    def setUp(self):

        User.query.delete()
        


        user = User(first_name = "test", last_name = "case")

        db.session.add(user)
        db.session.commit()

    def tearDown(self):

        db.session.rollback()

    def test_add_user(self):

        user = User(first_name = "canon", last_name = "wiseman")

        db.session.add(user)
        db.session.commit()

        all_users = User.query.filter_by(first_name = "canon").all()
        
        self.assertEquals(all_users, [user])

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get('/users/3')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>test case</h2>', html)





