from models import *
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()
Tag.query.delete()

# Add Users
alan = User(first_name='Alan', last_name='Alda')
joel = User(first_name='Joel', last_name='Burton')
jane = User(first_name='Jane', last_name='Smith')

# Add new objects to session
db.session.add_all([alan, joel, jane])

# Commit data to db
db.session.commit()


# Add Post
post_one = Post(title='First Post!', content='Oh, hai.', user_id=2)
post_two = Post(title='Yet Another Post', content='Here is the content.', user_id=2)
post_three = Post(title='Flask is Awesome', content='Flask is a lovely framework for building cool things.', user_id=2)

# Add new objects to session
db.session.add_all([post_one, post_two, post_three])

# Commit data to db
db.session.commit()


# Add Tags
tag_one = Tag(name='Fun')
tag_two = Tag(name='Even More')
tag_three = Tag(name='Not So Fun')

# Add new objects to session
db.session.add_all([tag_one, tag_two, tag_three])

# Commit data to db
db.session.commit()