from flask import Blueprint, jsonify, request


from src import db
from src.db.models import OrderDetails, ReversalOrder

status_controller = Blueprint("status_controller", __name__)


# Endpoint to create a new reversal order
@status_controller.route("/create_reversal", methods=["POST"])
def create_reversal_order():
    data = request.get_json()

    # Extract data from the request
    original_order_id = data.get("original_order_id")
    faulty_quantity = data.get("faulty_quantity")

    # Fetch the original order to link with
    original_order = OrderDetails.query.get(original_order_id)

    if not original_order:
        return jsonify({"message": "Original order not found!"}), 404

    # Create a new reversal order
    reversal_order = ReversalOrder(
        original_order_id=original_order_id,
        faulty_quantity=faulty_quantity,
        # Other necessary fields can be added here
    )

    db.session.add(reversal_order)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Reversal order created successfully!",
                "reversal_order_id": reversal_order.id,
            }
        ),
        201,
    )


# Other endpoints related to order status can be added here
