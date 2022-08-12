from models import User, Post, db, Tag
from app import app

#Create tables

db.drop_all()
db.create_all()


#empty tables

User.query.delete()
Post.query.delete()
Tag.query.delete()


# Add users

Jon = User(first_name = 'Jon', last_name = 'Smith')
Susan = User(first_name = 'Susan', last_name = 'Turner')
Hailey = User(first_name = 'Hailey', last_name = 'Hill')

db.session.add_all([Jon,Susan,Hailey])
db.session.commit()

# Add Posts

post_1 = Post(title = "test", content = "testing", user_id = 1)
post_2 = Post(title = "test 2", content = "testing twice", user_id = 2)
post_3 = Post(title = "This is a Title", content = "this is the content of the post", user_id = 2)

db.session.add_all([post_1, post_2, post_3])
db.session.commit()