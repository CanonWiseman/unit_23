"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

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

    def __repr__(self):
        """Show info about user."""

        u = self
        return f"<User {u.id} {u.first_name} {u.last_name}>"

