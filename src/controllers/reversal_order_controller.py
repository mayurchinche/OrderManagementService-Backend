from src.services.reversal_order_service import ReversalOrderService

class ReversalOrderController:
    @staticmethod
    def add_reversal_order(data):
        original_order_id=data.get('original_order_id')
        faulty_quantity=data.get('faulty_quantity')
        return ReversalOrderService.add_reversal_order(original_order_id, faulty_quantity)

    @staticmethod
    def update_reversal_status(data):
        reversal_order_id=data.get('reversal_order_id')
        status=data.get('status')
        dc_status=data.get('dc_status')
        return ReversalOrderService.update_reversal_status(reversal_order_id, status, dc_status)

    @staticmethod
    def get_all_reversal_orders():
        return ReversalOrderService.get_all_reversal_orders()

    @staticmethod
    def delete_reversal_order(data):
        reversal_order_id=data.get('reversal_order_id')
        return ReversalOrderService.delete_reversal_order(reversal_order_id)
