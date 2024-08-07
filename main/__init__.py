from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from os import path
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from dotenv import load_dotenv
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
DB_NAME = "Blog"
jwt = JWTManager()

def create_app():
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sgwdb3e821e3debef'
   # app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:Code1234@localhost:5000/{DB_NAME}'
    #app.config['JWT_SECRET_KEY'] = 'we3efef0323fehfuhfff'
    app.config['SQLALCHEMY_DATABASE_URI'] =  os.getenv('DATABASE_URL')
    db.init_app(app)
    migrate = Migrate(app,db)
    jwt.init_app(app)

    from .auth import auth
    from .post import post
    from .comment import comment
    
    app.register_blueprint(auth, url_prefix = '/auth')
    app.register_blueprint(post, url_prefix = '/post')
    app.register_blueprint(comment, url_prefix = '/comment')

    from .models import Users,Posts,Comments

    with app.app_context():
        db.create_all()
    
    
    return app

def create_database(app):
    if not path.exists('app/' + DB_NAME):
        with app.app_context:
            db.create_all(app=app)
        print('Created Database!')