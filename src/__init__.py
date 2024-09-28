from flask import Flask, jsonify
from src.routes import  main_routes
from src.docs.swagger import setup_swagger
from src.configs.config import Config
from src.exception import global_exception_handler
from flask_sqlalchemy import SQLAlchemy

from .db.db import  db

def create_app():
    app = Flask(__name__)

    print("Config Loaded")
    # Load configuration
    app.config.from_object(Config)
    db.init_app(app)

    # Register blueprints
    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from .routes import main_routes  # Import after initializing db to avoid circular import
    app.register_blueprint(main_routes, url_prefix='/src')

    with app.app_context():
            # Create tables if they do not exist
            db.create_all()
            print("All tables are created")
    # Setup Swagger (optional)
    setup_swagger(app)

    return app