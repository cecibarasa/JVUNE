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
    secure_password = db.Column(db.String(255),nullable = False)
    blogs = db.relationship('Blog',backref = 'user', lazy = 'dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    photos = db.relationship('PhotoProfile', backref='user', lazy="dynamic")
    
    def save_user(self):
        db.session.add(self)
        db.session.commit()
    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def set_password(self):
        raise AttributeError('You cannot read the password attribute')

    @set_password.setter
    def password(self, password):
        self.secure_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.secure_password,password) 
    
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
    blog_author = db.Column(db.String)
    blog_content = db.Column(db.String(1000))
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comments = db.relationship('Comment', backref='blog_id', lazy="dynamic")
    upvote = db.relationship('Upvote', backref='blog', lazy='dynamic')
    downvote = db.relationship('Downvote', backref='blog', lazy='dynamic')


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

class Upvote(db.Model):
    __tablename__ = 'upvotes'
    id = db.Column(db.Integer, primary_key=True)
    upvote = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
    def save(self):
        db.session.add(self)
        db.session.commit()
    def upvote(cls, id):
        upvote_blog = Upvote(user=current_user, blog_id=id)
        upvote_blog.save()
    @classmethod
    def query_upvotes(cls, id):
        upvote = Upvote.query.filter_by(blog_id=id).all()
        return upvote
    @classmethod
    def all_upvotes(cls):
        upvotes = Upvote.query.order_by('id').all()
        return upvotes
    def __repr__(self):
        return f'{self.user_id}:{self.blog_id}'
class Downvote(db.Model):
    __tablename__ = 'downvotes'
    id = db.Column(db.Integer, primary_key=True)
    downvote = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
    def save(self):
        db.session.add(self)
        db.session.commit()
    def downvote(cls, id):
        downvote_blog = Downvote(user=current_user, blog_id=id)
        downvote_blog.save()
    @classmethod
    def query_downvotes(cls, id):
        downvote = Downvote.query.filter_by(blog_id=id).all()
        return downvote
    @classmethod
    def all_downvotes(cls):
        downvote = Downvote.query.order_by('id').all()
        return downvote
    def __repr__(self):
        return f'{self.user_id}:{self.blog_id}'

class Subscriber(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(), unique = True)               
