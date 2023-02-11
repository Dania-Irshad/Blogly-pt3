from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

DEFAULT_PHOTO = "https://isobarscience.com/wp-content/uploads/2020/09/default-profile-picture1.jpg"

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text,
                           nullable=False)
    last_name = db.Column(db.Text,
                          nullable=False)
    image_url = db.Column(db.Text, nullable=False,
                          server_default=DEFAULT_PHOTO)

    def __repr__(self):
        """Show info about user."""
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"
    
    posts = db.relationship("Post", backref="users", cascade="all, delete-orphan")

class Post(db.Model):
    """Post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text,
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.Text, nullable=False,
                           default=datetime.now().strftime("%a %b %-d %Y, %I:%M %p"))
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        """Show info about post."""
        p = self
        return f"<Post {p.id} {p.title} {p.content} {p.created_at} {p.user_id}>"

class Tag(db.Model):
    """Tag"""

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text,
                      nullable=False, unique=True)

    posts = db.relationship("Post", secondary="posts_tags", backref="tags", cascade="all,delete")

class PostTag(db.Model):
    """PostTag"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey("posts.id", ondelete="CASCADE"), 
                        primary_key=True)
    tag_id = db.Column(db.Integer, 
                       db.ForeignKey("tags.id", ondelete="CASCADE"), 
                       primary_key=True)