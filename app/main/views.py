from flask import render_template, request, redirect,url_for
from . import main
from ..requests import get_quote

#views
@main.route('/')
def index():
    '''
    view root page that retunrs index page with its data
    '''
    title = 'JVUNE | Welcome to JVUNE Blogs'
    quote = get_quote()

    return render_template('index.html', title = title, quote = quote)