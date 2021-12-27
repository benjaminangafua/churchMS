
from os import path

from flask import Flask
from cs50 import SQL

db = SQL('sqlite:///church.db')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aglkghhfklahlhggakhfg'

    # Initialize database
    
    from .views import views
    app.register_blueprint(views, url_prefix='/')  
    return app

