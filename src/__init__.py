import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from src.routes import  main_routes
from src.docs.swagger import setup_swagger
from src.configs.config import Config
from src.exception import global_exception_handler
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .db.db import  db
from src.models import users,order_details,suppliers,materials,reversal_order,material_modules
from src.oms.routes import order_bp
from .logging.logging_handler import log_request, log_response
from flask_jwt_extended import JWTManager

load_dotenv()
def create_app():
    app = Flask(__name__)
    print("Loading all the configs, ......Loaded")
    # Load configuration
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)
    # Register blueprints
    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from .routes import main_routes  # Import after initializing db to avoid circular import
    app.register_blueprint(main_routes, url_prefix='/src')

    from .oms.routes import order_bp
    app.register_blueprint(order_bp)

    from .resources import material_blueprint
    app.register_blueprint(material_blueprint, url_prefix='/api')

    from .resources import customer_blueprint
    app.register_blueprint(customer_blueprint, url_prefix='/api')

    from .resources import suppliers_blueprint
    app.register_blueprint(suppliers_blueprint, url_prefix='/api')

    from src.resources import reversal_orders_blueprint
    app.register_blueprint(reversal_orders_blueprint, url_prefix='/api')

    from src.resources import order_blueprint

    app.register_blueprint(order_blueprint, url_prefix='/api')

    from src.core.routes import core_blueprint
    app.register_blueprint(core_blueprint, url_prefix='/api/core')

    from src.resources.module import module_bp
    app.register_blueprint(module_bp, url_prefix="/api")

    with app.app_context():
            # Create tables if they do not exist
            db.create_all()
            print("All tables are created")
    # Setup Swagger (optional)
    setup_swagger(app)

    app.config['JWT_SECRET_KEY'] = os.getenv('secret_key')
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    jwt = JWTManager(app)

    return app