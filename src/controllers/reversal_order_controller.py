from flask import Blueprint, request, jsonify

from src.db.models import ReversalOrder
from src.models.order_details import OrderDetails
from src import db

reversal_order_bp = Blueprint("reversal_order", __name__)

order_bp = Blueprint("order", __name__)

status_bp = Blueprint("status", __name__)


@status_bp.route("/update_order_status/<int:order_id>", methods=["PATCH"])
def update_order_status(order_id):
    """
    updateOrderStatus:
      patch:
        summary: Update the status of an order
        tags:
          - Orders
        parameters:
          - in: path
            name: order_id
            required: true
            description: ID of the order to update
            schema:
              type: integer
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  order_status:
                    type: string
                    description: New status of the order
        responses:
          200:
            description: Order status updated successfully
          404:
            description: Order not found

    """
    data = request.json
    order = OrderDetails.query.get(order_id)

    if not order:
        return jsonify({"message": "Order not found!"}), 404

    # Update the order status based on input
    new_status = data.get("order_status")
    order.order_status = new_status

    db.session.commit()
    return jsonify({"message": "Order status updated successfully!"}), 200


@status_bp.route("/update_reversal_order_status/<int:reversal_id>", methods=["PATCH"])
def update_reversal_order_status(reversal_id):
    data = request.json
    reversal_order = ReversalOrder.query.get(reversal_id)

    if not reversal_order:
        return jsonify({"message": "Reversal order not found!"}), 404

    # You can define statuses for reversal orders as needed
    new_status = data.get("status")  # e.g., "Received"
    reversal_order.status = new_status  # Assuming you have a status column

    db.session.commit()
    return jsonify({"message": "Reversal order status updated successfully!"}), 200


@order_bp.route("/orders", methods=["GET"])
def get_orders():
    orders = OrderDetails.query.all()
    order_list = [
        {
            "order_id": order.order_id,
            "user_contact_number": order.user_contact_number,
            "reversal_orders": [
                {
                    "reversal_id": reversal.reversal_id,
                    "faulty_quantity": reversal.faulty_quantity,
                    "reversal_reason": reversal.reversal_reason,
                }
                for reversal in order.reversal_orders
            ],
            **{
                column.name: getattr(order, column.name, None)
                for column in order.__table__.columns
            },
        }
        for order in orders
    ]
    return jsonify(order_list)


@reversal_order_bp.route("/create_reversal_order", methods=["POST"])
def create_reversal_order():
    data = request.json
    original_order_id = data.get("original_order_id")
    faulty_quantity = data.get("faulty_quantity")
    reversal_reason = data.get("reversal_reason")

    # Create the reversal order
    new_reversal_order = ReversalOrder(
        original_order_id=original_order_id,
        faulty_quantity=faulty_quantity,
        reversal_reason=reversal_reason,
    )
    db.session.add(new_reversal_order)

    # Optionally update the original order status if needed
    original_order = OrderDetails.query.get(original_order_id)
    if original_order:
        original_order.is_reversed = True

    db.session.commit()
    return jsonify({"message": "Reversal order created successfully!"}), 201
