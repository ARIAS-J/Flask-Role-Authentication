from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_user import UserManager
from os import path



db = SQLAlchemy()

DB_NAME = "loginform.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'loginkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['USER_ENABLE_EMAIL'] = False
    db.init_app(app)
    
    
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    
    from .models import User
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    user_manager = UserManager(app, db, User)
    
    return app

def create_database(app):
    if not path.exists('loginform/' + DB_NAME):
        db.create_all(app=app)
        print('Create Database')