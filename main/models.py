from . import db
from sqlalchemy.sql import func

class Users(db.Model):
    __tablename__ = 'Users'

    user_id = db.Column(db.Integer(), primary_key= True, autoincrement = True)
    username = db.Column(db.String(30), nullable=False, unique = True)
    email = db.Column(db.String(50), unique=True,nullable=False)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=True)
    registeredTime = db.Column(db.DateTime(timezone=True), default=func.now(),nullable=False)
    posts = db.relationship('Posts', back_populates='author')
    comments = db.relationship('Comments', back_populates='author')


class Posts(db.Model):
    __tablename__ = 'Posts'

    post_id = db.Column(db.Integer(), primary_key= True, autoincrement = True)
    author_id = db.Column(db.Integer(), db.ForeignKey(Users.user_id))
    title = db.Column(db.String(80),nullable=False)
    content = db.Column(db.String(1500), nullable=False,unique = True)
    image = db.Column(db.String(255),nullable = True)  
    mimetype = db.Column(db.String(60), nullable = True)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(),onupdate=func.now(),nullable = True)
    author = db.relationship('Users', back_populates='posts')
    comments = db.relationship('Comments', back_populates='post')



class Comments(db.Model):
    __tablename__ = 'Comments'

    comment_id = db.Column(db.Integer(), primary_key= True, autoincrement = True)
    post_id = db.Column(db.Integer(), db.ForeignKey(Posts.post_id))
    user_id = db.Column(db.Integer(), db.ForeignKey(Users.user_id))
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(),onupdate=func.now(),nullable = True)
    post = db.relationship('Posts', back_populates='comments')
    author = db.relationship('Users', back_populates='comments')
