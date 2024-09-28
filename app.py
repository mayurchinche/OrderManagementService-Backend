from flask import Flask
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

api = Api(app)


# Swagger UI configuration
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  # Path to your Swagger JSON file
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "My Flask API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# Dummy user data
users = {
    "testuser": "password123"  # In a real app, use a database
}

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if username in users and users[username] == password:
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"message": "Invalid credentials"}), 401

api.add_resource(Login, '/login')



if __name__ == '__main__':
    app.run(debug=True)
