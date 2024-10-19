from src.constants.order_status import OrderStatus
from src.controllers.order_controller import OrderController


class POService:

    @staticmethod
    def fetch_delivery_pending_orders():
        OrderController.get_all_orders(status=OrderStatus.ORDER_PLACED)

    @staticmethod
    def raise_po(order_id,data):
        # Logic for PO team to raise a PO and change status to ORDER_PENDING
        return OrderController.raise_po(order_id, data)

    @staticmethod
    def update_order_delivery(order_id,data):
        # Logic to mark the order as delivered
        return OrderController.update_order(order_id,status=OrderStatus.ORDER_DELIVERED,data=data)
