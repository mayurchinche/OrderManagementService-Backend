from functools import wraps

from flask import Blueprint, request

from src.constants.roles import Roles
from src.constants.order_status import OrderStatus
from src.core.services.approval_service import ApprovalService
from src.core.services.order_service import OrderService
from src.core.services.po_service import POService
from src.core.services.reversal_order_service import ReversalOrderService
from src.core.services.analysis_service import AnalysisService

from src.sequrity.decorators import  apply_decorators

core_blueprint = Blueprint('core', __name__)



@core_blueprint.route("/orders/add_order", methods=['POST'])
@apply_decorators()
def add_order():
    """
    Add Order
    ---
    tags:
      - Employee Resource
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
            - model
            - customer_name
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
            model:
              type: string
              description: Model of the material
            customer_name:
              type: string
              description: Name of the customer

    responses:
      201:
        description: Order added successfully
    """
    data = request.get_json()

    return OrderService.add_order(data)


@core_blueprint.route("/orders/ordered_by/<string:contact_number>", methods=['GET'])
@apply_decorators()
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
@apply_decorators(allowed_roles=Roles.ONLY_MANAGER)
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
@apply_decorators()
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
@apply_decorators()
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
@apply_decorators(allowed_roles=Roles.ONLY_PO_TEAM)
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
            - ordered_price
            - po_raised_by
            - supplier_name
          properties:
            po_no:
              type: integer
              description: purchase order number
            ordered_price:
              type: float
              description: Ordered price
            po_raised_by:
              type: string
              description: PO Team member who raised the PO
            supplier_name:
              type: string
              description: Name of the supplier
    responses:
      200:
        description: List of all orders
    """
    data = request.get_json()
    data["status"] = OrderStatus.ORDER_PLACED
    return POService.raise_po(order_id, data)


@core_blueprint.route("/orders/delivery/<int:order_id>", methods=['PUT'])
@apply_decorators(allowed_roles=Roles.ONLY_PO_TEAM)
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
        name: body
        schema:
          type: object
          required:
            - received_date
            - received_quantity
          properties:
            received_date:
              type: string
              description: Date when the order was delivered
            received_quantity:
              type: integer
              description: Number of items received

    responses:
      200:
        description: Order marked as delivered
      404:
        description: Order not found
    """
    data = request.get_json()
    data["status"] = OrderStatus.ORDER_DELIVERED
    return POService.update_order_delivery(order_id, data)


@core_blueprint.route("/orders/approve/<int:order_id>", methods=['PUT'])
@apply_decorators(allowed_roles=Roles.ONLY_MANAGER)
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
    data["status"] = OrderStatus.REVIEW_PENDING
    return ApprovalService.approve_order(order_id, data)


@core_blueprint.route("/orders/review_pending", methods=['GET'])
@apply_decorators()
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


@core_blueprint.route("/orders/add_reversal_order", methods=['POST'])
@apply_decorators()
def add_reversal_order():
    """
    Add Reversal Order
    ---
    tags:
      - Employee Resource
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
    return ReversalOrderService.add_reversal_order(data)


@core_blueprint.route("/orders/reversal/get_all_reversal_orders", methods=['GET'])
@apply_decorators()
def get_all_reversal_orders():
    """
    Get Reversal Orders
    ---
    tags:
      -  Manager Resource
    responses:
      200:
        description: List of reversal orders
    """
    return ReversalOrderService.get_reversal_orders()


@core_blueprint.route("/orders/reversal/get_reversal_orders/<string:user_contact_number>", methods=['GET'])
@apply_decorators()
def get_reversal_order_by_user(user_contact_number):
    """
    Get Reversal Orders For Logged-In User
    ---
    tags:
      - Employee Resource
    parameters:
      - in: path
        name: user_contact_number
        required: true
        type: string
        description: user_contact_number
    responses:
      200:
        description: List of reversal orders
    """
    return ReversalOrderService.get_reversal_orders(user_contact_number=user_contact_number)


@core_blueprint.route("/orders/reversal/approve_reversal_order/<int:reversal_order_id>", methods=['PUT'])
@apply_decorators(allowed_roles=Roles.ONLY_MANAGER)
def approve_reversal_order(reversal_order_id):
    """
    Approve Order
    ---
    tags:
      - Manage Orders
    operationId: put_api_approve_reversal_order
    parameters:
      - in: path
        name: reversal_order_id
        required: true
        type: integer
        description: ID of the reversal order to approve
      - in: body
        name: body
        schema:
          type: object
          required:
            - reversal_order_id
          properties:
            reversal_order_id:
              type: integer
              description: ID of the reversal order
    responses:
      200:
        description: Reversal Order approved successfully
      404:
        description: Reversal Order not found
    """

    data = {
        "status": OrderStatus.DC_PENDING
    }
    return ReversalOrderService.update_reversal_status(reversal_order_id, data)


@core_blueprint.route("/orders/reversal/get_reversal_review_pending", methods=['GET'])
@apply_decorators()
def get_reversal_review_pending_orders():
    """
    Get Review Pending Orders
    ---
    tags:
      - Manage Orders
    responses:
      200:
        description: List of review pending orders
    """
    return ReversalOrderService.get_reversal_orders(status=OrderStatus.REVERSAL_REVIEW_PENDING)


@core_blueprint.route("/orders/reversal/get_dc_pending", methods=['GET'])
@apply_decorators()
def get_dc_pending_orders():
    """
    Get DC Pending Orders
    ---
    tags:
      - PO Resource
    responses:
      200:
        description: List of DC pending orders
    """
    return ReversalOrderService.get_reversal_orders(status=OrderStatus.DC_PENDING)


@core_blueprint.route("/orders/reversal/submit_dc_for_reversal/<int:reversal_order_id>", methods=['PUT'])
@apply_decorators(allowed_roles=Roles.ONLY_PO_TEAM)
def submit_dc_for_reversal(reversal_order_id):
    """
    Raise Delivery Chalan
    ---
    tags:
      - PO Resource
    parameters:
      - in: path
        name: reversal_order_id
        required: true
        type: integer
        description: ID of the reversal order to Submit Delivery Chalan
      - in: body
        name: body
        schema:
          type: object
          required:
            - dc_number
          properties:
            dc_number:
              type: string
              description: Delivery Chalan Number
    responses:
      200:
        description: Submit Dc for Reversal Order
    """
    data = {
        "status": OrderStatus.REVERSAL_ORDER_PLACED,
        "dc_number": request.get_json().get('dc_number')
    }
    return ReversalOrderService.update_reversal_status(reversal_order_id=reversal_order_id, data=data)


@core_blueprint.route("/orders/reversal/get_reversal_delivery_pending_orders", methods=['GET'])
@apply_decorators()
def get_reversal_delivery_pending_orders():
    """
    Get Reversal Delivery Pending Orders
    ---
    tags:
      - PO Resource
    responses:
      200:
        description: List of Reversal Delivery pending orders
    """
    return ReversalOrderService.get_reversal_orders(status=OrderStatus.REVERSAL_ORDER_PLACED)


@core_blueprint.route("/orders/revrsal/delivery/<int:reversal_order_id>", methods=['PUT'])
@apply_decorators(allowed_roles=Roles.ONLY_PO_TEAM)
def mark_reversal_order_delivered(reversal_order_id):
    """
    Mark Reversal Order as Delivered
    ---
    tags:
      - PO Resource
    parameters:
      - in: path
        name: reversal_order_id
        required: true
        type: integer
        description: ID of the order to mark as delivered
      - in : body
        name: delivered_at
        schema:
          type: object
          required:
            - delivered_at
          properties:
            delivered_at:
              type: string
              description: Date when the reversal order was delivered

    responses:
      200:
        description: Reversal Order marked as delivered
      404:
        description: Order not found
    """
    data = request.get_json()
    data["status"] = OrderStatus.REVERSAL_ORDER_DELIVERED

    return ReversalOrderService.update_reversal_status(reversal_order_id, data)


@core_blueprint.route("/api/cost-analysis/highlights", methods=['GET'])
@apply_decorators()
def get_cost_analysis_highlights():
    """
       Get cost analysis highlights
       ---
       tags:
         - Analysis Resource
       parameters:
         - in: query
           name: start_date
           required: true
           type: string
           description: Start Date
         - in: query
           name: end_date
           required: true
           type: string
           description: End Date
       responses:
         200:
           description: Highlights Details
       """
    return AnalysisService.get_cost_analysis_highlights(start_date=request.args.get('start_date'),end_date=request.args.get('end_date'))


@core_blueprint.route("/api/cost-analysis/get_price_trend", methods=['GET'])
@apply_decorators()
def get_price_trend():
    """
       Get get_price_trend
       ---
       tags:
         - Analysis Resource
       parameters:
         - in: query
           name: start_date
           required: true
           type: string
           description: Start Date
         - in: query
           name: end_date
           required: true
           type: string
           description: End Date
         - in: query
           name: interval
           required: false
           type: string
           description: By Default Interval is daily specify if monthly
       responses:
         200:
           description: Highlights Details
       """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    interval = request.args.get('interval', 'daily')  # Default to daily

    return AnalysisService.get_price_trend(start_date, end_date,interval)