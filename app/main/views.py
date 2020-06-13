from flask import render_template, request, redirect,url_for
from . import main
from ..requests import get_quote
from flask_login import login_required

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

    return render_template('profile/profile.html',user = user, title=title)    