from models import User, Post, db
from app import app

#Create tables

db.drop_all()
db.create_all()

#empty tables

User.query.delete()
Post.query.delete()

# Add users

Jon = User(first_name = 'Jon', last_name = 'Smith')
Susan = User(first_name = 'Susan', last_name = 'Turner')
Hailey = User(first_name = 'Hailey', last_name = 'Hill')

db.session.add_all([Jon,Susan,Hailey])
db.session.commit()