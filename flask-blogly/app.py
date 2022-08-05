"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "1234"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route("/")
def home_page():

    return redirect("/users")

@app.route("/users", methods=['GET'])
def users_page():
    """returns a list of all users"""

    users = User.query.all()

    return render_template("users_page.html", users=users)

@app.route("/users/new", methods=['GET'])
def user_form():
    """returns form for creating user"""
    return render_template('users_form.html')

@app.route("/users/new", methods=['POST'])
def process_form():
    """Processes form and adds the new user to database"""
    
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']
    image_url = str(image_url) if image_url else None

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route("/users/<int:user_id>")
def show_user_details(user_id):
    """Displays individual user page"""

    user = User.query.get_or_404(user_id)
    return render_template("user_profile.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["GET"])
def show_user_edit(user_id):
    """Returns form to edit users information"""

    user = User.query.get_or_404(user_id)
    return render_template("user_edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Updates user information in the database"""
    
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['image-url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Deletes selected user from database"""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

    

    

    