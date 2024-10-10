from flask import Flask
from src.auth.routes import auth_bp
from src.docs.swagger import setup_swagger


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object("app.configs.Config")

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # Setup Swagger (optional)
    setup_swagger(app)

    return app
