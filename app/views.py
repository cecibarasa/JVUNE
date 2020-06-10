from flask import render_template
from app import app

#views
@app.route('/')
def index():
    '''
    view root page that retunrs index page with its data
    '''

    return render_template('index.html')