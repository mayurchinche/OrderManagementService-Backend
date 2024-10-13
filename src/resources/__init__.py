from flask import Blueprint
from flask_restful import Api
from src.resources.material_resource import MaterialResource
from src.resources.supplier_resource import SupplierResource

# Create a Blueprint for the materials module
material_blueprint = Blueprint('materials', __name__)
material_api = Api(material_blueprint)

# Register MaterialResource with the Blueprint
material_api.add_resource(MaterialResource, '/materials')


suppliers_blueprint = Blueprint('suppliers', __name__)
suppliers_api = Api(suppliers_blueprint)

suppliers_api.add_resource(SupplierResource, '/suppliers')
