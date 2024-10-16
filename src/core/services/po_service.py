from src.controllers.order_controller import OrderController


class POService:
    @staticmethod
    def raise_po(order_id,data):
        # Logic for PO team to raise a PO and change status to ORDER_PENDING
        return OrderController.raise_po(order_id,data)

    @staticmethod
    def update_order_delivery(order_id):
        # Logic to mark the order as delivered
        return OrderController.update_order_status_to_delivered(order_id)
