from flask import jsonify
from flask_jwt_extended import jwt_required

from app import app
from src.models import OrderDetails


@app.route("/cost-effectiveness", methods=["GET"])
@jwt_required()
def get_cost_effectiveness():
    orders = OrderDetails.query.all()
    order_list = [
        {
            "order_id": order.order_id,
            "expected_price": order.expected_price,
            "negotiated_price": order.negotiated_price,
            "cost_savings_percentage": order.calculate_cost_effectiveness(),
        }
        for order in orders
    ]
    return jsonify(order_list), 200


# controller/cost_effectiveness_controller.py


def calculate_cost_effectiveness(order):
    """
    Compares the manager's expected price with the price negotiated by the PO team.
    Returns a cost-effectiveness score or a simple performance message.
    """
    expected_price = order.expected_price
    actual_price = order.actual_price

    if actual_price is None or expected_price is None:
        return "Pricing data incomplete."

    if actual_price < expected_price:
        performance = "Cost effective"
        savings = expected_price - actual_price
    elif actual_price == expected_price:
        performance = "On budget"
        savings = 0
    else:
        performance = "Over budget"
        savings = expected_price - actual_price  # Negative savings

    return {
        "performance": performance,
        "expected_price": expected_price,
        "actual_price": actual_price,
        "savings": savings,
    }
