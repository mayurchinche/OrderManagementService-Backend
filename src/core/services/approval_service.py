from src.constants.order_status import OrderStatus
from src.controllers.order_controller import OrderController


class ApprovalService:
    @staticmethod
    def approve_order(order_id, data):
        # Validate and approve the order, updating status to PO_PENDING
        return OrderController.approve_order(order_id, data)

    @staticmethod
    def get_review_pending_orders():
        # Get all orders with Review_Pending status
        return OrderController.get_all_orders(status=OrderStatus.REVIEW_PENDING)

