from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin,current_user
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Quote:

    def __init__(self, author, quote):
        self.author = author
        self.quote = quote

class User(UserMixin,db.Model):
    
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), index = True)
    email = db.Column(db.String(255),unique = True, index = True)
    bio = db.Column(db.String(1000))
    profile_pic_path = db.Column(db.String)
    password_hash = db.Column(db.String(255))
    blogs = db.relationship('Blog',backref = 'user', lazy = 'dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    photos = db.relationship('PhotoProfile',backref = 'user',lazy = "dynamic")
    
    @property
    def set_password(self):
        raise AttributeError('You cannot read the password attribute')
    @set_password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash,password) 
    def save_u(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def __repr__(self):
        return f'User {self.username}'

class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))        

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer,primary_key = True)
    blog_title = db.Column(db.String)
    blog_content = db.Column(db.String(1000))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comments = db.relationship('Comment',backref =  'blog_id',lazy = "dynamic")


    def save_blog(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_blog(cls,id):
        blog = Blog.query.filter_by(id = id).first()

        return blog

    def __repr__(self):
        return f'Blog {self.blog_title}'


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(1000))
    name = db.Column(db.String)
    blog = db.Column(db.Integer,db.ForeignKey("blogs.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,blog):
        comments = Comment.query.filter_by(blog_id = blog).all()
        return comments

    @classmethod
    def delete_comment(cls,id):
        comment = Comment.query.filter_by(id=id).first()
        db.session.delete(comment)
        db.session.commit()

    def __repr__(self):
        return f'Comment{self.comment}'
