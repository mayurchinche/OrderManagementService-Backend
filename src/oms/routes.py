import logging

from flask_jwt_extended import get_jwt_identity

from src.logging.logging_handler import log_request, log_response
from flask import Blueprint, request, jsonify
from src.exception.global_exception_handler import handle_exception
from src.oms import service as oms_service
from src.sequrity.decorators import jwt_required_with_contact_validation, custom_jwt_required

order_bp = Blueprint('order', __name__)

# Add a new order

@order_bp.route('/add_new_order', methods=['POST'])
@log_request
@log_response
@jwt_required_with_contact_validation
@handle_exception
def add_new_order():
    """
    Add a new order to the order_details table.
    ---
    tags:
      - Orders
    summary: "Add new order"
    description: "This endpoint adds a new order to the order_details table."
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: "JWT token in the format 'Bearer {token}'"
      - name: order
        in: body
        required: true
        schema:
          type: object
          required:
                - contact_number
          properties:
            contact_number:
              type: string
              description: "Contact number of the logged in user"
            user_contact_number:
              type: string
              description: "Contact number of the user placing the order"
            name_of_customer:
              type: string
              description: "Name of the customer"
            ordered_quantity:
              type: integer
              description: "Quantity of items ordered"
            materials:
              type: string
              description: "Materials related to the order"
            model:
              type: string
              description: "Model associated with the order"
            order_to:
              type: string
              description: "Who the order is placed with"
            order_date:
              type: string
              format: date
              description: "Date when the order was placed"
            received_date:
              type: string
              format: date
              description: "Date when the order was received"
            pending_quantity:
              type: integer
              description: "Quantity of items still pending"
    responses:
      201:
        description: Order added successfully
        schema:
          type: object
          properties:
            message:
              type: string
              description: "Success message"
            order_id:
              type: integer
              description: "ID of the newly created order"
    consumes:
      - application/json
    produces:
      - application/json
    """
    data = request.get_json()
    return oms_service.add_order(data)


# Get all orders placed by a specific user
@order_bp.route('/get-orders', methods=['GET'])
@log_request
@log_response
@jwt_required_with_contact_validation
@handle_exception
def get_orders():
    """
        Get all orders placed by the user.
        ---
        tags:
          - Orders
        summary: "Get orders by user"
        description: "This endpoint retrieves all orders placed by the user based on their contact number."
        parameters:
          - name: Authorization
            in: header
            type: string
            required: true
            description: "JWT token in the format 'Bearer {token}'"
          - name: contact_number
            in: query
            type: string
            required: true
            description: The contact number of the user
        responses:
          200:
            description: A list of orders
            schema:
              type: array
              items:
                properties:
                  order_id:
                    type: integer
                  user_contact_number:
                    type: string
                  name_of_customer:
                    type: string
                  order_date:
                    type: string
                    format: date
        produces:
          - application/json
        """
    contact_number = request.args.get('contact_number')
    return oms_service.get_orders_by_user(contact_number)

# Show all orders
@order_bp.route('/show-all-orders', methods=['GET'])
@log_request
@log_response
@jwt_required_with_contact_validation
@handle_exception
def show_all_orders():
    """
    Show all orders.
    ---
    tags:
      - Orders
    summary: "Show all orders"
    description: "This endpoint retrieves all orders in the system."
    parameters:
          - name: Authorization
            in: header
            type: string
            required: true
            description: "JWT token in the format 'Bearer {token}'"
          - name: contact_number
            in: query
            type: string
            required: true
            description: The contact number of the user
    responses:
      200:
        description: A list of all orders
        schema:
          type: array
          items:
            properties:
              order_id:
                type: integer
              user_contact_number:
                type: string
              name_of_customer:
                type: string
              order_date:
                type: string
                format: date
    consumes:
      - application/json
    produces:
      - application/json
    """
    return oms_service.show_all_orders()

# Add a new column to the order_details table
@order_bp.route('/add-column', methods=['PUT'])
@log_request
@log_response
@jwt_required_with_contact_validation
@handle_exception
def add_column():
    """
    Add a new column to the order_details table.
    ---
    tags:
      - Orders
    summary: "Add a new column to the order_details table"
    description: "This endpoint adds a new column to the order_details table with the specified name and type."
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: "JWT token in the format 'Bearer {token}'"
      - name: Column_Details
        in: body
        required: true
        schema:
          type: object
          required:
                - contact_number
                - Column_Name
          properties:
            contact_number:
              type: string
              description: "Contact Number of login user"
            Column_Name:
              type: string
              description: "New column to be added this would be added with type as varchar(255)"
    responses:
      200:
        description: Column added successfully
        schema:
          type: object
          properties:
            message:
              type: string
              description: "Success message"
    consumes:
      - application/json
    produces:
      - application/json
    """
    column_name = request.json.get('Column_Name')
    print("column_name",column_name)
    return oms_service.add_new_column(column_name )
