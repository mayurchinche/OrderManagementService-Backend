from flask import jsonify, request

from src.services.order_service import OrderService

class OrderController:
    @staticmethod
    def get_all_orders(status=None,contact_number=None, limit=None, offset=None):
        try:
            orders = OrderService.get_orders(status,contact_number, limit, offset)
            return {"data": [order.to_dict() for order in orders]}, 200
        except Exception as e:
            return {"message": f"Error fetching orders: {str(e)}"}, 500
    @staticmethod
    def add_order(material_name, order_date, order_quantity, ordered_by, user_contact_number):
        return OrderService.add_order(material_name, order_date, order_quantity, ordered_by,user_contact_number)

    @staticmethod
    def update_order(order_id, status=None,po_no=None,data=None, approved_by=None):
        return OrderService.update_order(order_id, approved_by)

    @staticmethod
    def delete_order(order_id):
        return OrderService.delete_order(order_id)

    # @staticmethod
    # def get_review_pending_orders():
    #     try:
    #         orders = OrderService.get_review_pending_orders()
    #         return {"status": "success", "data": orders}, 200
    #     except Exception as e:
    #         return {"status": "fail", "message": str(e)}, 500
    #
    # @staticmethod
    # def approve_order(order_id,data):
    #     response, status_code = OrderService.approve_order(order_id, data)
    #     return response, status_code

    @staticmethod
    def raise_po(order_id,data):
        print(data)
        return OrderService.update_order(order_id,data)