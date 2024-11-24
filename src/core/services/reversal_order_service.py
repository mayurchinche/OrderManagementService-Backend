from src.controllers.reversal_order_controller import ReversalOrderController


class ReversalOrderService:
    def __init__(self):
        pass
    @staticmethod
    def get_reversal_orders(status=None,user_contact_number=None):
        print("contact_number",user_contact_number)
        return ReversalOrderController.get_reversal_orders(status=status,user_contact_number=user_contact_number)

    @staticmethod
    def add_reversal_order(data):
        return ReversalOrderController.add_reversal_order(data)

    @staticmethod
    def update_reversal_status(reversal_order_id=None,data=None):
        return ReversalOrderController.update_reversal_status(reversal_order_id,data)

    @staticmethod
    def delete_reversal_order(reversal_order_id):
        return ReversalOrderController.delete_reversal_order(reversal_order_id)