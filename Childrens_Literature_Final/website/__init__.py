from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os 

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app(config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'a_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .routes import routes
    app.register_blueprint(routes, url_prefix='/')

    from .models.database import User, Prompt, Story
    create_database(app)

    return app

def create_database(app):
    if not os.path.exists(DB_NAME):  # just check current folder
        with app.app_context():
            db.create_all()
        print("Database created!")
