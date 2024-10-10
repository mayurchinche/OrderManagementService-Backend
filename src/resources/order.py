from flask import Blueprint, request, jsonify

from .. import order_bp
from ..db.db import db
from ..db.models import OrderDetails
from ..services import order_service
from ..utils.decorators import jwt_required_with_contact_validation, role_required

bp = Blueprint("orders", __name__, url_prefix="/orders")


@bp.route("/add-order", methods=["POST"])
@jwt_required_with_contact_validation
@order_bp.route("/add-order", methods=["POST"])
@role_required("Employee")
def add_order():
    data = request.json

    try:
        # Extract the necessary fields from the request data
        new_order = OrderDetails(
            order_date=data.get("order_date"),
            name_of_customer=data.get("name_of_customer"),
            po_no_or_whatsapp_date=data.get("po_no_or_whatsapp_date"),
            materials=data.get("materials"),
            model=data.get("model"),
            ordered_quantity=data.get("ordered_quantity"),
            order_to=data.get("order_to"),
            ordered_by=data.get("ordered_by"),
            pending_quantity=data.get("pending_quantity"),
            status="Review_Pending",  # Initial status as 'Review Pending'
        )

        # Add the new order to the database
        db.session.add(new_order)
        db.session.commit()

        return jsonify({"message": "Order added successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


def view_orders():
    """
    View all orders
            ---
            tags:
              - Orders
            parameters:
              - in: header
                name: Authorization
                required: true
                description: JWT token for user authorization
              - in: query
                name: user_contact_number
                schema:
                  type: string
                  description: Contact number to filter orders by user
            responses:
              200:
                description: Successfully fetched the orders!
              401:
                description: Unauthorized, JWT token is invalid or missing.
              500:
                description: Server error occurred while fetching orders.
    """
    pass


def update_order_status():
    """
    Update order status
            ---
            tags:
              - Orders
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
                      description: The ID of the order to update
                    status:
                      type: string
                      description: New status of the order (e.g., 'Order Placed', 'Order Delivered')
            responses:
              200:
                description: Order status updated successfully!
              400:
                description: Invalid input, Please check your request.
              401:
                description: Unauthorized, JWT token is invalid or missing.
              500:
                description: Server error occurred while updating the order status.
    """
    pass


@order_bp.route("/review-order/<int:order_id>", methods=["PUT"])
@role_required("Manager")
def review_order(order_id):
    data = request.json

    # Fetch the order based on order_id
    order = OrderDetails.query.filter_by(order_id=order_id).first()

    if not order:
        return jsonify({"message": "Order not found!"}), 404

    try:
        # Update order status and additional details added by the manager
        order.approved_by = data.get("approved_by")
        order.ordered_quantity = data.get("ordered_quantity")
        order.status = "PO_Pending"  # After review, status will be 'PO Pending'

        db.session.commit()

        return jsonify({"message": "Order reviewed and approved successfully!"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@order_bp.route("/place-order/<int:order_id>", methods=["PUT"])
@role_required("PO_Team")
def place_order(order_id):
    data = request.json

    # Fetch the order based on order_id
    order = OrderDetails.query.filter_by(order_id=order_id).first()

    if not order:
        return jsonify({"message": "Order not found!"}), 404

    try:
        # Place order with supplier and update status
        order.ordered_price = data.get("ordered_price")
        order.status = "Order_Placed"

        db.session.commit()

        return jsonify({"message": "Order placed successfully!"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@order_bp.route("/track-order/<int:order_id>", methods=["GET"])
@role_required("Employee", "Manager", "PO_Team")
def track_order(order_id):
    # Fetch the order based on order_id
    order = OrderDetails.query.filter_by(order_id=order_id).first()

    if not order:
        return jsonify({"message": "Order not found!"}), 404

    # Logic to calculate TAT (Turnaround Time) and assign color
    # You can add the logic to calculate based on current date and order's expected delivery date
    tat_color = calculate_tat_color(order)

    return jsonify(
        {
            "order_id": order.order_id,
            "name_of_customer": order.name_of_customer,
            "order_date": order.order_date,
            "status": order.status,
            "tat_color": tat_color,
        }
    )


from datetime import datetime, timedelta


def calculate_tat_color(order):
    current_date = datetime.now().date()
    tat_days = 10  # Example TAT is 10 days
    order_date = order.order_date
    tat_start = order_date + timedelta(days=5)  # Yellow (pending)
    tat_end = order_date + timedelta(days=tat_days)  # Red (past TAT)

    if current_date <= tat_start:
        return "Yellow"
    elif tat_start < current_date <= tat_end:
        return "Orange"
    elif current_date > tat_end:
        return "Red"
    return "Green"


@order_bp.route("/create-reversal-order", methods=["POST"])
@role_required("Employee", "Manager")
def create_reversal_order():
    data = request.json

    try:
        # Create a new reversal order linked to the original order
        reversal_order = OrderDetails(
            original_order_id=data.get("original_order_id"),
            materials=data.get("materials"),
            faulty_quantity=data.get("faulty_quantity"),
            status="Reversal_Order_Placed",
        )

        db.session.add(reversal_order)
        db.session.commit()

        return jsonify({"message": "Reversal order created successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
