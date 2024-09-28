from flask_swagger_ui import get_swaggerui_blueprint

def setup_swagger(app):
    SWAGGER_URL = '/api/docs'  # URL for accessing the Swagger UI
    API_URL = '/static/swagger.json'  # Path to the Swagger JSON file

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "OMS Web-App with Swagger"
        }
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
