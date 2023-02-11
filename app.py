from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "sec_ret$0987"
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def home_page():
    return render_template("homepage.html")

@app.route("/users")
def list_users():
    """Display all users"""
    users = User.query.all()
    return render_template("users/users.html", users=users)

@app.route("/users/new")
def new_user():
    """Display new user form."""
    return render_template("users/new.html")

@app.route("/users/new", methods=["POST"])
def get_user():
    """Add new user and redirect to users"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users")

@app.route("/users/<int:user_id>")
def user_detail(user_id):
    """Display details of the user"""
    user = User.query.get_or_404(user_id)
    return render_template("users/detail.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["GET"])
def edit_user(user_id):
    """Display edit user form."""
    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def get_updated_user(user_id):
    """Edit user and redirect to detail page"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete user and redirect to homepage"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")



@app.route("/users/<int:user_id>/posts/new")
def new_post(user_id):
    """Display new post form"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("posts/new.html", user=user, tags=tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def get_post(user_id):
    """Add post and redirect to user detail page"""
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']
    tags_list = [int(num) for num in request.form.getlist('tags')]
    post_tags = Tag.query.filter(Tag.id.in_(tags_list)).all()
    post = Post(title=title, content=content, user_id=user.id, tags=post_tags)
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    """Display details of the post"""
    post = Post.query.get_or_404(post_id)
    return render_template("posts/detail.html", post=post)

@app.route("/posts/<int:post_id>/edit", methods=["GET"])
def edit_post(post_id):
    """Display edit post form."""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("posts/edit.html", post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def get_updated_post(post_id):
    """Edit post and redirect to post detail page"""
    title = request.form['title']
    content = request.form['content']
    tags_list = [int(num) for num in request.form.getlist('tags')]
    post = Post.query.get(post_id)
    post.title = title
    post.content = content
    post.tags = Tag.query.filter(Tag.id.in_(tags_list)).all()
    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post_id}")

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete post and redirect to user detail page"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")



@app.route("/tags")
def list_tags():
    """List all tags"""
    tags = Tag.query.all()
    return render_template("tags/tags.html", tags=tags)

@app.route("/tags/new")
def new_tag():
    """Display new tag form"""
    posts = Post.query.all()
    return render_template("tags/new.html", posts=posts)

@app.route("/tags/new", methods=["POST"])
def get_tag():
    """Add tag and redirect to tags list"""
    name = request.form['name']
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return redirect("/tags")

@app.route("/tags/<int:tag_id>")
def tag_detail(tag_id):
    """Display details of tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tags/detail.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit")
def tags_edit_form(tag_id):
    """Display edit tag form"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tags/edit.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Edit post and redirect to tags list"""
    tag = Tag.query.get_or_404(tag_id)
    name = request.form['name']
    tag.name = name
    db.session.add(tag)
    db.session.commit()
    return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete tag and redirect to tags list"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")