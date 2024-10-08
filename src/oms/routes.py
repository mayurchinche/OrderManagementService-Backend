import logging

from flask_jwt_extended import get_jwt_identity
from sqlalchemy import inspect

from src.db.db import db
from src.logging.logging_handler import log_request, log_response
from flask import Blueprint, request, jsonify, current_app
from src.exception.global_exception_handler import handle_exception
from src.models.order_details import OrderDetails
from src.oms import service as oms_service
from src.sequrity.decorators import jwt_required_with_contact_validation, custom_jwt_required
from sqlalchemy import text
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


@order_bp.route('/update_order', methods=['PUT'])
@log_request
@log_response
@handle_exception
@jwt_required_with_contact_validation
def update_order():
    """
    Update order status or pending quantity.
    ---
    tags:
      - Orders
    summary: "Update order"
    description: "This endpoint allows updating the order-status or pending_quantity for a specific order."
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: "JWT token in the format 'Bearer {token}'"
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - order_id
          properties:
            order_id:
              type: integer
              description: "The order ID to update."
            order_status:
              type: string
              description: "The new status of the order."
            pending_quantity:
              type: integer
              description: "The updated pending quantity."
    responses:
      200:
        description: "Order updated successfully."
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Order updated successfully."
      400:
        description: "Bad request."
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid data provided."
      500:
        description: "Internal server error."
        schema:
          type: object
          properties:
            error:
              type: string
              example: "An internal error occurred."
    """
    data = request.get_json()
    order_id = data.get('order_id')
    order_status = data.get('order_status')
    pending_quantity = data.get('pending_quantity')

    if not order_id:
        return jsonify({"error": "Order ID is required."}), 400

    return oms_service.update_order(order_id,order_status,pending_quantity )

@order_bp.route('/get-all-columns', methods=['GET'])
def get_all_columns():
    """
    Retrieves all columns dynamically from the OrderDetails table
    ---
    tags:
      - Orders
    summary: "Get all columns in OrderDetails table"
    description: "Retrieves all orders with dynamic columns, including newly added columns."
    responses:
      200:
        description: "List of orders with dynamic columns"
        schema:
          type: array
          items:
            properties:
              order_id:
                type: integer
              user_contact_number:
                type: string
              dynamic_columns:
                type: object
                description: "A dictionary of dynamically added columns"
    """
    inspector = inspect(db.engine)

    # Get all columns for the order_details table
    columns = [column['name'] for column in inspector.get_columns('order_details')]

    # Return the list of column names
    return jsonify({"columns": columns})

@order_bp.route('/describe-order-table', methods=['GET'])
def describe_order_table():
    """
    Get all columns of the OrderDetails table
    ---
    tags:
      - Orders
    summary: "Get all columns of the OrderDetails table"
    description: "This endpoint retrieves all the column names and their types dynamically from the OrderDetails table, even if new columns are added."
    responses:
      200:
        description: A list of columns with their names and types
        schema:
          type: array
          items:
            properties:
              name:
                type: string
                description: The name of the column
              type:
                type: string
                description: The type of the column
      500:
        description: Internal Server Error
    """
    try:
        # Get the table inspector
        inspector = inspect(db.engine)
        # Use reflection to get the columns of the order_details table
        columns = inspector.get_columns('order_details')

        # Prepare the column info as a response
        column_info = []
        for column in columns:
            column_info.append({
                'name': column['name'],
                'type': str(column['type'])
            })
        print("column_info", column_info)
        # Return the column information
        return jsonify(column_info), 200

    except Exception as e:
        current_app.logger.error(f"Error describing table: {str(e)}")
        return jsonify({"error": "Unable to describe table"}), 500


@order_bp.route('/get-order-details', methods=['GET'])
def get_order_details():
    """
    Get order details including dynamically added columns
    ---
    tags:
      - Orders
    summary: "Get order details including all columns"
    description: "Fetch all order details, including any newly added columns dynamically."
    parameters:
      - name: order_id
        in: query
        type: integer
        required: true
        description: The ID of the order to fetch
    responses:
      200:
        description: Order details with all columns
        schema:
          type: object
          additionalProperties:
            type: string
      404:
        description: Order not found
    """
    try:
        # Get the order_id from query parameters
        order_id = request.args.get('order_id')

        # Use reflection to get the columns of the order_details table
        inspector = inspect(db.engine)
        columns = inspector.get_columns('order_details')

        # Dynamically build the query to fetch the order details, including new columns
        query = db.session.query(OrderDetails).filter_by(order_id=order_id).first()

        if not query:
            return jsonify({"error": "Order not found"}), 404

        # Dynamically build a dictionary of column values
        result = {}
        for column in columns:
            result[column['name']] = getattr(query, column['name'], None)

        return jsonify(result), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching order details: {str(e)}")
        return jsonify({"error": "Unable to fetch order details"}), 500


@order_bp.route('/get-orders-updated', methods=['GET'])
def get_orders_updated():
    """
    Retrieve all orders.
    ---
    tags:
      - Orders
    summary: "Get all orders updated"
    description: "This endpoint retrieves all orders in the system, including dynamically added columns."
    responses:
      200:
        description: A list of orders
        schema:
          type: array
          items:
            type: object
            properties:
              order_id:
                type: integer
                description: "The unique identifier of the order"
              user_contact_number:
                type: string
                description: "The contact number of the user"
              name_of_customer:
                type: string
                description: "The name of the customer"
              po_no_or_whatsapp_date:
                type: string
                format: date
                description: "Purchase order number or WhatsApp date"
              materials:
                type: string
                description: "Materials ordered"
              model:
                type: string
                description: "Model number of the product"
              ordered_quantity:
                type: integer
                description: "The quantity ordered"
              order_to:
                type: string
                description: "Order placed to which supplier"
              order_date:
                type: string
                format: date
                description: "The date of the order"
              received_date:
                type: string
                format: date
                description: "The date the order was received"
              pending_quantity:
                type: integer
                description: "The remaining quantity to be fulfilled"
              # You can add more fields here, including dynamically added ones.
              additional_properties:
                type: object
                description: "Other dynamic fields if present"
        examples:
          application/json:
            - order_id: 1
              user_contact_number: "+919657491288"
              name_of_customer: "John Doe"
              po_no_or_whatsapp_date: "2024-09-21"
              materials: "Steel"
              model: "XYZ123"
              ordered_quantity: 100
              order_to: "ABC Suppliers"
              order_date: "2024-09-20"
              received_date: "2024-09-22"
              pending_quantity: 20
    """
    inspector = inspect(db.engine)

    # Get all columns for the order_details table
    columns = [column['name'] for column in inspector.get_columns('order_details')]

    # Perform a raw SQL query to fetch all rows and columns
    orders = db.session.execute(text(f'SELECT * FROM order_details')).fetchall()

    # Create a list to hold the orders data
    results = []

    # Iterate through the result set and prepare a dictionary for each row
    for order in orders:
        result = {column: getattr(order, column) for column in columns}
        results.append(result)

    # Return all orders with their columns dynamically fetched
    return jsonify(results)


@order_bp.route('/add-dynamic-order', methods=['PUT'])
@log_request
@log_response
def add_dynamic_order():
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
                order_status:
                  type: string
                  description: "Status of order"
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
    data=request.get_json()

    return oms_service.add_dynamic_order(data)