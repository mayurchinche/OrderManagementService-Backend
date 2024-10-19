from flask import request
from flask_restful import Resource

from src.controllers.reversal_order_controller import ReversalOrderController


class ReversalOrderResource(Resource):
    def __init__(self):
        self.controller = ReversalOrderController

    @staticmethod
    def post():
        """
        Add Reversal Order
        ---
        tags:
          - Reversal Orders
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - original_order_id
                - reversal_quantity
                - origin_order_supplier_name
                - original_order_quantity
                - user_contact_number
                - description
                - created_at
                - original_order_material_name
              properties:
                original_order_id:
                  type: integer
                  description: ID of the original order
                reversal_quantity:
                  type: integer
                  description: Number of faulty items
                origin_order_supplier_name:
                  type: string
                  description: Name of the supplier
                original_order_quantity:
                  type: integer
                  description: Quantity of faulty items
                user_contact_number:
                  type: string
                  description: Contact number of the user
                description:
                  type: string
                  description: Description of the reversal
                created_at:
                  type: string
                  description: Date of creation
                original_order_material_name:
                  type: string
                  description: Name of the material
        responses:
          201:
            description: Reversal order added successfully
        """
        data = request.get_json()
        return ReversalOrderController.add_reversal_order(data)

    @staticmethod
    def put():
        """
        Update Reversal Order Status
        ---
        tags:
          - Reversal Orders
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - reversal_order_id
                - status
              properties:
                reversal_order_id:
                  type: integer
                  description: ID of the reversal order
                status:
                  type: string
                  description: New status for the reversal order
                dc_status:
                  type: string
                  description: Optional DC status
        responses:
          200:
            description: Reversal order updated successfully
        """
        data = request.get_json()
        return ReversalOrderController.update_reversal_status(data)

    @staticmethod
    def get():
        """
        Get All Reversal Orders
        ---
        tags:
          - Reversal Orders
        responses:
          200:
            description: List of all reversal orders
        """
        return ReversalOrderController.get_reversal_orders()

    @staticmethod
    def delete():
        """
        Delete Reversal Order
        ---
        tags:
          - Reversal Orders
        parameters:
          - in: query
            name: reversal_order_id
            required: true
            type: integer
            description: ID of the reversal order to delete
        responses:
          200:
            description: Reversal order deleted successfully
        """
        data = request.get_json()
        return ReversalOrderController.delete_reversal_order(data)
