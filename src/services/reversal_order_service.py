from src.db.db import db
from src.models.reversal_order import ReversalOrder

class ReversalOrderService:
    @staticmethod
    def add_reversal_order(original_order_id, faulty_quantity):
        new_reversal = ReversalOrder(
            original_order_id=original_order_id,
            faulty_quantity=faulty_quantity,
            status="Reversal_Pending"
        )
        db.session.add(new_reversal)
        db.session.commit()
        return {"status": "success", "message": "Reversal order added successfully!"}

    @staticmethod
    def update_reversal_status(reversal_order_id, status, dc_status=None):
        reversal_order = ReversalOrder.query.get(reversal_order_id)
        if not reversal_order:
            return {"status": "fail", "message": "Reversal order not found!"}
        reversal_order.status = status
        if dc_status:
            reversal_order.dc_status = dc_status
        db.session.commit()
        return {"status": "success", "message": "Reversal order updated successfully!"}

    @staticmethod
    def get_all_reversal_orders():
        reversal_orders = ReversalOrder.query.all()
        return [
            {
                "id": ro.id,
                "original_order_id": ro.original_order_id,
                "faulty_quantity": ro.faulty_quantity,
                "status": ro.status,
                "dc_status": ro.dc_status
            } for ro in reversal_orders
        ]

    @staticmethod
    def delete_reversal_order(reversal_order_id):
        reversal_order = ReversalOrder.query.get(reversal_order_id)
        if not reversal_order:
            return {"status": "fail", "message": "Reversal order not found!"}
        db.session.delete(reversal_order)
        db.session.commit()
        return {"status": "success", "message": "Reversal order deleted successfully!"}
