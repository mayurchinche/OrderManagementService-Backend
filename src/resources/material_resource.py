from flask import request
from flask_restful import Resource, reqparse

from src.constants.roles import Roles
from src.controllers.material_controller import MaterialController
from src.sequrity.decorators import apply_decorators
class MaterialResource(Resource):
    def __init__(self):
        self.controller = MaterialController()

    @staticmethod
    @apply_decorators()
    def get():
        """
        Get All Materials
        ---
        tags:
          - Materials
        responses:
          200:
            description: Successfully fetched all materials
          500:
            description: Error fetching materials
        """
        return MaterialController.get_all_materials()

    @staticmethod
    @apply_decorators(allowed_roles=[Roles.ONLY_MANAGER])
    def post():
        """
        Add New Material
        ---
        tags:
          - Materials
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - material_name
                - description
              properties:
                material_name:
                  type: string
                  description: Name of the material
                description:
                  type: string
                  description: Description of the material
        responses:
          201:
            description: Material successfully added
          400:
            description: Material already exists
          500:
            description: Error adding material
        """
        try:
            # Extract data from request body
            data = request.get_json()
            # Call the controller to add material
            return MaterialController.add_material(data)

        except Exception as e:
            return {"message": f"Failed to add material: {str(e)}"}, 500

    @staticmethod
    @apply_decorators(allowed_roles=[Roles.ONLY_MANAGER])
    def delete():
        """
        Delete Material
        ---
        tags:
          - Materials
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - material_name
              properties:
                material_name:
                  type: string
                  description: name of the material to delete
        responses:
          200:
            description: Material successfully deleted
          404:
            description: Material not found
          500:
            description: Error deleting material
        """
        parser = reqparse.RequestParser()
        parser.add_argument("material_name", type=str, required=True, help="Material name cannot be blank!")
        args = parser.parse_args()

        return MaterialController.delete_material(args["material_name"])
