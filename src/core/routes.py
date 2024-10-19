from flask import Blueprint, request
from src.core.services.order_service import OrderService
from src.core.services.approval_service import ApprovalService
from src.core.services.po_service import POService

core_blueprint = Blueprint('core', __name__)

@core_blueprint.route("/orders/ordered_by/<string:contact_number>", methods=['GET'])
def get_employee_orders(contact_number):
    """
    Get All Orders for logged-in user
    ---
    tags:
      - Employee Resource
    parameters:
      - in: path
        name: contact_number
        required: false
        type: string
        description: contact_number for user_specific orders
    responses:
      200:
        description: List of all orders
    """
    return OrderService.fetch_employee_orders(contact_number)

@core_blueprint.route("/orders/get_all_orders", methods=['GET'])
def get_all_orders():
    """
    Get All Orders
    ---
    tags:
      - Manager Resource
    responses:
      200:
        description: List of all orders
      500:
        description: Internal Server Error
    """
    return OrderService.fetch_all_orders()


@core_blueprint.route("/orders/get_po_pending_orders", methods=['GET'])
def get_po_pending_orders():
    """
    Get All PO_PENDING Orders
    ---
    tags:
      - PO Resource
    responses:
      200:
        description: List of all orders
      500:
        description: Internal Server Error
    """
    return OrderService.fetch_po_pending_orders()


@core_blueprint.route("/orders/get_delivery_pending_orders", methods=['GET'])
def get_delivery_pending_orders():
    """
    Get All Delivery Pending Orders
    ---
    tags:
      - PO Resource
    responses:
      200:
        description: List of all delivery pending orders
      500:
        description: Internal Server Error
    """
    return OrderService.fetch_delivery_pending_orders()

@core_blueprint.route("/orders/raise_po/<int:order_id>", methods=['POST'])
def raise_po(order_id):
    """
    Raise Po for po pending order
    ---
    tags:
      - PO Resource
    parameters:
      - in: path
        name: order_id
        required: false
        type: integer
        description: ID of the order for which PO is raised
      - in: body
        name: body
        schema:
          type: object
          required:
            - po_no
            - supplier_id
            - ordered_price
            - po_raised_by
          properties:
            po_no:
              type: integer
              description: purchase order number
            supplier_id:
              type: integer
              description: Supplier ID
            ordered_price:
              type: float
              description: Ordered price
            po_raised_by:
              type: string
              description: PO Team member who raised the PO
    responses:
      200:
        description: List of all orders
    """
    data=request.get_json()
    return POService.raise_po(order_id,data)

@core_blueprint.route("/orders/delivery/<int:order_id>", methods=['PUT'])
def mark_order_delivered(order_id):
    """
    Mark Order as Delivered
    ---
    tags:
      - PO Resource
    parameters:
      - in: path
        name: order_id
        required: true
        type: integer
        description: ID of the order to mark as delivered

      - in : body
        name: received_date
        schema:
          type: object
          required:
            - received_date
          properties:
            received_date:
              type: string
              description: Date when the order was delivered
    responses:
      200:
        description: Order marked as delivered
      404:
        description: Order not found
    """
    data=request.get_json()
    return POService.update_order_delivery(order_id,data)


@core_blueprint.route("/orders/approve/<int:order_id>", methods=['PUT'])
def approve_order(order_id):
    """
    Approve Order
    ---
    tags:
      - Manage Orders
    operationId: put_api_approve_order
    parameters:
      - in: path
        name: order_id
        required: true
        type: integer
        description: ID of the order to approve
      - in: body
        name: body
        schema:
          type: object
          required:
            - order_quantity
            - expected_price
            - approved_by
          properties:
            order_quantity:
              type: integer
              description: Updated order quantity
            expected_price:
              type: float
              description: Expected price for the order
            approved_by:
              type: string
              description: Manager who approved the order
    responses:
      200:
        description: Order approved successfully
      404:
        description: Order not found
    """
    data = request.get_json()
    return ApprovalService.approve_order( order_id, data)


@core_blueprint.route("/orders/review_pending", methods=['GET'])
def get_review_pending_orders():
    """
    Get Review Pending Orders
    ---
    tags:
      - Manage Orders
    responses:
      200:
        description: List of review pending orders
    """
    return ApprovalService.get_review_pending_orders()
