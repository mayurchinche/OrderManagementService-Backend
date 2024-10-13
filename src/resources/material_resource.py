from flask import request
from flask_restful import Resource, reqparse
from src.controllers.material_controller import MaterialController

class MaterialResource(Resource):
    def __init__(self):
        self.controller = MaterialController()

    @staticmethod
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
                - material_id
              properties:
                material_id:
                  type: integer
                  description: ID of the material to delete
        responses:
          200:
            description: Material successfully deleted
          404:
            description: Material not found
          500:
            description: Error deleting material
        """
        parser = reqparse.RequestParser()
        parser.add_argument("material_id", type=int, required=True, help="Material ID cannot be blank!")
        args = parser.parse_args()

        return MaterialController.delete_material(args["material_id"])
