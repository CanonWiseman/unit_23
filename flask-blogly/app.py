"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Post, Tag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "1234"

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

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
def handle_user_form():
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
    posts = Post.query.filter_by(user_id = user_id)

    return render_template("user_profile.html", user=user, posts=posts)

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

@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def show_post_form(user_id):
    """Shows the form for adding a post for a user"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template("post_form.html", user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def handle_new_post(user_id):
    """handle users new post. add post to database and connect it to correct user"""

    user = User.query.get_or_404(user_id)

    title = request.form['title']
    content = request.form['content']
    posted_by = user.id
    tags = request.form.getlist('tags')
    print(tags)

    new_post = Post(title = title, content = content, user_id = posted_by)

    for tag in tags:
        new_post.tags.append(tag)

    db.session.add(new_post) 
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """shows the details of selected post"""

    post = Post.query.get_or_404(post_id)

    return render_template("post_page.html", post=post)

@app.route('/posts/<int:post_id>/edit', methods=["GET"])
def show_post_edit(post_id):
    """Display form to edit current post"""

    post = Post.query.get_or_404(post_id)

    return render_template("post_edit.html", post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_post_edit(post_id):
    """Process post edits and update in database"""

    post = Post.query.get_or_404(post_id)

    if request.form["title"]:
        post.title = request.form['title']
    else:
        post.title = post.title

    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Deletes selected post from database"""

    post = Post.query.get_or_404(post_id)
    user_id = post.user.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')
    
@app.route('/tags', methods = ["GET"])
def show_tags():
    """Displays tag page with all tags"""
    
    tags = Tag.query.all()

    return render_template('tag_page.html', tags=tags)

@app.route('/tags/<int:tag_id>', methods = ["GET"])
def show_tag_details(tag_id):
    """Displays individual tag with all correlating posts"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag_detail.html', tag=tag)

@app.route('/tags/new', methods = ["GET"])
def tag_create_form():
    """displays form to create a new tag"""

    return render_template("tag_form.html")

@app.route('/tags/new', methods = ["POST"])
def handle_tag_form():
    """Process new tag"""

    tag_name = request.form["name"]

    new_tag = Tag(name = tag_name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit', methods=["GET"])
def show_tag_edit(tag_id):
    """Displays form to edit current tag"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template("tag_edit.html", tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def handle_tag_edit(tag_id):
    """handles tag edit form and updates it in the database"""

    tag = Tag.query.get_or_404(tag_id)

    if request.form["name"]:
        tag.name = request.form["name"]

    db.session.add(tag)
    db.session.commit()
    
    return redirect(f'/tags/{tag.id}')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Deletes current tag from database"""
    
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')




    

    