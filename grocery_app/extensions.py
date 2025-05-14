from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# Set login view
login_manager.login_view = 'auth.login'

def init_app(app):
    """Initialize Flask extensions with the app."""
    # Initialize SQLAlchemy
    db.init_app(app)
    
    # Initialize Flask-Bcrypt
    bcrypt.init_app(app)
    
    # Initialize Flask-Login
    login_manager.init_app(app)

    from grocery_app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))