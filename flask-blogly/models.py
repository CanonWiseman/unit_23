"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    first_name = db.Column(db.Text, nullable = False)

    last_name = db.Column(db.Text, nullable = False)

    image_url = db.Column(db.Text, nullable = True, default = "https://t3.ftcdn.net/jpg/03/46/83/96/360_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws.jpg")

    posts = db.relationship('Post', backref = "user", cascade = "all, delete-orphan")

    def __repr__(self):
        """Show info about user."""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name}>"



class Tag(db.Model):
    """Tags model"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    name = db.Column(db.String(20), nullable = False, unique = True)

class Post(db.Model):
    """Post model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    title = db.Column(db.String(50), nullable = False)

    content = db.Column(db.Text, nullable = False)

    created_at = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable = False)
    
    related_tags = db.relationship('PostTag', backref = "post")

    tags = db.relationship("Tag", secondary = 'post_tags', backref = 'posts')

class PostTag(db.Model):
    """joining table for tags and posts"""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True)





