from flask import request, jsonify
from flask_restful import Resource

from src.constants.roles import Roles
from src.controllers.supplier_controller import SupplierController
from src.sequrity.decorators import apply_decorators
class SupplierResource(Resource):

    @apply_decorators(allowed_roles=Roles.ONLY_PO_TEAM)
    def post(self):
        """
                Add a new Supplier
                ---
                tags:
                  - Suppliers
                parameters:
                  - in: body
                    name: body
                    schema:
                      type: object
                      required:
                        - supplier_name
                        - contact_number
                      properties:
                        supplier_name:
                          type: string
                          description: The name of the supplier
                        contact_number:
                          type: string
                          description: Contact details of the supplier
                responses:
                  201:
                    description: Supplier added successfully!
                  400:
                    description: Supplier already exists
                  500:
                    description: Internal server error
        """
        try:
            # Extract data from request body
            data = request.get_json()
            # Call the controller to add supplier
            # Return the response from the controller
            return SupplierController.add_supplier(data)

        except Exception as e:
            return jsonify({"message": f"Failed to add supplier: {str(e)}"}, 500)

    @staticmethod
    @apply_decorators()
    def get():
        """
        Get All Suppliers
        ---
        tags:
          - Suppliers
        responses:
          200:
            description: Successfully fetched all Suppliers
          500:
            description: Error fetching Suppliers
        """
        return SupplierController.get_all_supplier()