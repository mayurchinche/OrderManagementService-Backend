from flask import request
from src.constants import order_status
from src.constants.order_status import OrderStatus

from src.controllers.order_controller import OrderController


class OrderService:
    @staticmethod
    def fetch_employee_orders(contact_number):
        # Logic to get orders belonging to a specific employee
        return OrderController.get_all_orders(contact_number=contact_number)

    @staticmethod
    def fetch_all_orders():
        # Logic to get all orders that the manager can view
        return OrderController.get_all_orders()

    @staticmethod
    def fetch_po_pending_orders():
        return OrderController.get_all_orders(status=OrderStatus.PO_PENDING)

    @staticmethod
    def fetch_delivery_pending_orders():
        return OrderController.get_all_orders(status=OrderStatus.ORDER_PLACED)