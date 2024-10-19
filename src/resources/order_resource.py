from flask import request
from flask_restful import Resource

from src.controllers.order_controller import OrderController


class OrderResource(Resource):

    @staticmethod
    def get():
        """
        Get All Orders
        ---
        tags:
          - Orders Resource
        parameters:
          - in: query
            name: status
            required: false
            type: string
            description: Filter orders by status
          - in: contact_number
            name: contact_number
            required: false
            type: string
            description: contact_number for user_specific orders
          - in: query
            name: limit
            required: false
            type: integer
            description: Limit the number of orders returned
          - in: query
            name: offset
            required: false
            type: integer
            description: Offset for pagination
        responses:
          200:
            description: List of all orders
        """
        status = request.args.get("status")
        contact_number = request.args.get("contact_number")
        limit = request.args.get("limit", type=int)
        offset = request.args.get("offset", type=int)

        return OrderController.get_all_orders(status,contact_number, limit, offset)

    @staticmethod
    def post():
        """
        Add Order
        ---
        tags:
          - Orders Resource
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - material_name
                - order_date
                - order_quantity
                - ordered_by
                - user_contact_number
              properties:
                material_name:
                  type: string
                  description: Name of the material
                order_date:
                  type: string
                  description: Date when the order is placed
                order_quantity:
                  type: integer
                  description: Quantity of the material
                ordered_by:
                  type: string
                  description: Name of the person who ordered
                user_contact_number:
                  type: string
                  description: contact_number of the person who ordered

        responses:
          201:
            description: Order added successfully
        """
        data = request.get_json()
        material_name = data.get("material_name")
        order_date = data.get("order_date")
        order_quantity = data.get("order_quantity")
        ordered_by = data.get("ordered_by")
        user_contact_number = data.get("user_contact_number")

        return OrderController.add_order(material_name, order_date, order_quantity, ordered_by, user_contact_number)

    @staticmethod
    def put():
        """
        Update Order Status
        ---
        tags:
          - Orders Resource
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - order_id
                - status
              properties:
                order_id:
                  type: integer
                  description: ID of the order
                status:
                  type: string
                  description: New status for the order
                approved_by:
                  type: string
                  description: Name of the person approving the order
        responses:
          200:
            description: Order updated successfully
        """
        data = request.get_json()
        order_id = data.get("order_id")
        return OrderController.update_order(order_id, data)

    @staticmethod
    def delete():
        """
        Delete Order
        ---
        tags:
          - Orders Resource
        parameters:
          - in: query
            name: order_id
            required: true
            type: integer
            description: ID of the order to delete
        responses:
          200:
            description: Order deleted successfully
        """
        order_id = request.args.get('order_id', type=int)
        return OrderController.delete_order(order_id)

#
# class ManageOrderResource(Resource):
#     @staticmethod
#     def get():
#         """
#         Get Review Pending Orders
#         ---
#         tags:
#           - Manage Orders
#         responses:
#           200:
#             description: List of review pending orders
#         """
#         return OrderController.get_review_pending_orders()
#
#
#     def put(self,order_id):
#         """
#         Approve Order
#         ---
#         tags:
#           - Manage Orders
#         parameters:
#           - in: path
#             name: order_id
#             required: true
#             type: integer
#             description: ID of the order to approve
#           - in: body
#             name: body
#             schema:
#               type: object
#               required:
#                 - order_quantity
#                 - expected_price
#                 - approved_by
#               properties:
#                 order_quantity:
#                   type: integer
#                   description: Updated order quantity
#                 expected_price:
#                   type: float
#                   description: Expected price for the order
#                 approved_by:
#                   type: string
#                   description: Manager who approved the order
#         responses:
#           200:
#             description: Order approved successfully
#           404:
#             description: Order not found
#         """
#         data = request.get_json()
#         return OrderController.approve_order(
#             order_id,
#             data
#         )
#
# class GetReviewPendingOrdersResource(Resource):
#     @staticmethod
#     def get():
#         """
#         Get Review Pending Orders
#         ---
#         tags:
#           - Manage Orders
#         responses:
#           200:
#             description: List of review pending orders
#         """
#         return OrderController.get_review_pending_orders()
#
# class ApproveOrderResource(Resource):
#     def put(self, order_id):
#         """
#         Approve Order
#         ---
#         tags:
#           - Manage Orders
#         operationId: put_api_approve_order
#         parameters:
#           - in: path
#             name: order_id
#             required: true
#             type: integer
#             description: ID of the order to approve
#           - in: body
#             name: body
#             schema:
#               type: object
#               required:
#                 - order_quantity
#                 - expected_price
#                 - approved_by
#               properties:
#                 order_quantity:
#                   type: integer
#                   description: Updated order quantity
#                 expected_price:
#                   type: float
#                   description: Expected price for the order
#                 approved_by:
#                   type: string
#                   description: Manager who approved the order
#         responses:
#           200:
#             description: Order approved successfully
#           404:
#             description: Order not found
#         """
#         data = request.get_json()
#         return OrderController.approve_order(order_id, data)
