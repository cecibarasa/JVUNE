from flask import Flask

#Initializing the application
app = Flask(__name__)

from app import views
