from flask import render_template, request, redirect,url_for,abort
from . import main
from ..requests import get_quote
from flask_login import login_required,current_user
from .forms import UpdateProfile,BlogForm,CommentForm
from .. import db
from ..models import User,Blog,Comment,PhotoProfile

#views
@main.route('/')
def index():
    '''
    view root page that retunrs index page with its data
    '''
    title = 'JVUNE | Welcome to JVUNE Blogs'
    quote = get_quote()

    return render_template('index.html', title=title, quote=quote)    
    
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    title = f"{uname.capitalize()}'s Profile"

    if user is None:
        abort(404)

    return render_template('profile/profile.html', user=user, title=title)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        user_photo = PhotoProfile(pic_path = path,user = user)
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/blogs/new', methods = ['GET','POST'])
@login_required
def new_blog():
    
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        blog = form.text.data

        new_blog = Blog(blog_title = title,blog_content = blog, user = current_user)
        new_blog.save_blog()

        return redirect(url_for('main.blogs'))

    title = 'New Blog'
    return render_template('new_blog.html',blog_form=form)

@main.route('/blog/comment/delete/<int:id>', methods = ['GET', 'POST'])
@login_required
def delete_comment(id):
    comment = Comment.query.filter_by(id=id).first()
    blog_id = comment.blog
    Comment.delete_comment(id)

    return redirect(url_for('main.blog',id=blog_id))

@main.route('/blog/<int:id>', methods = ["GET","POST"])
def blog(id):
    blog = Blog.get_blog(id)
    posted_date = blog.posted.strftime('%b %d, %Y')

    form = CommentForm()
    if form.validate_on_submit():
        comment = form.text.data
        name = form.name.data

        new_comment = Comment(comment = comment, name = name, blog_id = blog)

        new_comment.save_comment()

    comments = Comment.get_comments(blog)

    return render_template('blog.html', blog = blog, comment_form = form,comments = comments, date = posted_date)

@main.route('/user/<uname>/blogs', methods = ['GET','POST'])
def user_blogs(uname):
    user = User.query.filter_by(username = uname).first()
    blogs = Blog.query.filter_by(user_id = user.id).all()

    return render_template('profile/blogs.html', user = user, blogs = blogs)

@main.route('/blogs', methods = ['GET','POST'])
def blogs():
    blogs = Blog.query.order_by(Blog.id.desc()).limit(5)

    return render_template('blogs.html',blogs = blogs)

@main.route('/blog/<int:id>/update', methods = ['GET','POST'])
@login_required
def update_blog(id):
    
    blog = Blog.get_blog(id)
    form = BlogForm()
    if form.validate_on_submit():
        blog.blog_title = form.title.data
        blog.blog_content = form.text.data
        
        db.session.commit()
        return redirect(url_for('main.blogs', id = id))
    elif request.method == 'GET':
        form.title.data = blog.blog_title
        form.text.data = blog.blog_content
    
    return render_template('new_blog.html', blog_form = form, id=id)                     