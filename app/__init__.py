from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress FSADeprecationWarning

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    # Configure login manager
    login_manager.login_view = 'main.login'  # Redirect users to the login page if not authenticated
    login_manager.login_message_category = 'info'  # Bootstrap class for flash message

    # Import and register blueprints
    from .routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app

# Import models after db initialization to avoid circular import issues
from . import models

