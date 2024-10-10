from flask import Blueprint, request, jsonify
from src.services.order_service import OrderService

order_bp = Blueprint("order", __name__)


@order_bp.route("/order/<int:order_id>/status", methods=["PUT"])
def update_order_status(order_id):
    data = request.json
    new_status = data.get("status")
    updated_order = OrderService.update_order_status(order_id, new_status)
    if updated_order:
        return jsonify({"message": "Order status updated", "order": updated_order}), 200
    return jsonify({"message": "Order not found"}), 404


@order_bp.route("/order/reversal", methods=["POST"])
def create_reversal_order():
    data = request.json
    original_order_id = data.get("original_order_id")
    faulty_quantity = data.get("faulty_quantity")
    new_reversal_order = OrderService.create_reversal_order(
        original_order_id, faulty_quantity
    )
    if new_reversal_order:
        return (
            jsonify({"message": "Reversal order created", "order": new_reversal_order}),
            201,
        )
    return jsonify({"message": "Original order not found"}), 404
