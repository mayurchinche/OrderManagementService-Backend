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
                - faulty_quantity
              properties:
                original_order_id:
                  type: integer
                  description: ID of the original order
                faulty_quantity:
                  type: integer
                  description: Number of faulty items
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
        return ReversalOrderController.get_all_reversal_orders()

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
