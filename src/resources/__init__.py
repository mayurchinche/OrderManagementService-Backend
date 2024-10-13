from flask import Blueprint
from flask_restful import Api
from src.resources.material_resource import MaterialResource

# Create a Blueprint for the materials module
material_blueprint = Blueprint('materials', __name__)
material_api = Api(material_blueprint)

# Register MaterialResource with the Blueprint
material_api.add_resource(MaterialResource, '/materials')

