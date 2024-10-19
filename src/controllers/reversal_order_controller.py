from src.services.reversal_order_service import ReversalOrderService

class ReversalOrderController:
    @staticmethod
    def add_reversal_order(data):
        return ReversalOrderService.add_reversal_order(data)

    @staticmethod
    def update_reversal_status(reversal_order_id=None,data=None):
        return ReversalOrderService.update_reversal_status(reversal_order_id,data)

    @staticmethod
    def get_reversal_orders(status=None,user_contact_number=None):
        reversal_orders= ReversalOrderService.get_reversal_orders(status,user_contact_number)
        return {"data": [reversal_order.to_dict() for reversal_order in reversal_orders]},200

    @staticmethod
    def delete_reversal_order(data):
        reversal_order_id=data.get('reversal_order_id')
        return ReversalOrderService.delete_reversal_order(reversal_order_id)
