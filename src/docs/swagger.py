from flasgger import Swagger

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Order Management System API",
        "description": "API documentation for the Order Management System",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "api_key": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT token in the format 'Bearer {token}'"
        },
        "role": {
            "type": "apiKey",
            "name": "role",
            "in": "header",
            "description": "Role of the user"
        }
    },
    "security": [
        {
            "api_key": [],
            "role": []
        }
    ]
}
def setup_swagger(app):
    Swagger(app, template=swagger_template)
