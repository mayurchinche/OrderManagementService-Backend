from flask import jsonify, request

from src.services.order_service import OrderService

class OrderController:
    @staticmethod
    def add_order(material_name, order_date, order_quantity, ordered_by, user_contact_number):
        return OrderService.add_order(material_name, order_date, order_quantity, ordered_by,user_contact_number)

    @staticmethod
    def update_order(order_id, status, approved_by=None):
        return OrderService.update_order(order_id, status, approved_by)

    @staticmethod
    def delete_order(order_id):
        return OrderService.delete_order(order_id)

    @staticmethod
    def get_review_pending_orders():
        try:
            orders = OrderService.get_review_pending_orders()
            return {"status": "success", "data": orders}, 200
        except Exception as e:
            return {"status": "fail", "message": str(e)}, 500

    @staticmethod
    def approve_order(order_id,data):
        response, status_code = OrderService.approve_order(order_id, data)
        return response, status_code