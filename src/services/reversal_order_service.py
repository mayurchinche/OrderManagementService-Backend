from src.constants.order_status import OrderStatus
from src.db.db import db
from src.models.reversal_order import ReversalOrder

class ReversalOrderService:
    @staticmethod
    def add_reversal_order(data):
        new_reversal = ReversalOrder(
            original_order_id=data.get('original_order_id'),
            reversal_quantity=data.get('reversal_quantity'),
            user_contact_number=data.get('user_contact_number'),
            description=data.get('description'),
            created_at=data.get('created_at'),
            origin_order_supplier_name=data.get('origin_order_supplier_name'),
            original_order_quantity=data.get('original_order_quantity'),
            original_order_material_name=data.get('original_order_material_name'),
            status=OrderStatus.REVERSAL_REVIEW_PENDING
        )
        db.session.add(new_reversal)
        db.session.commit()
        return {"status": "success", "message": "Reversal order added successfully!"}

    @staticmethod
    def update_reversal_status(reversal_order_id=None,data=None):
        print("Reversal Delivery",data)
        if not reversal_order_id and not data:
            return {"status": "fail", "message": "Reversal order not found!"}
        if not reversal_order_id:
            reversal_order_id = data.get('reversal_order_id')
        reversal_order = ReversalOrder.query.get(reversal_order_id)
        if not reversal_order:
            return {"status": "fail", "message": "Reversal order not found!"}
        if reversal_order.status == OrderStatus.REVERSAL_REVIEW_PENDING and data['status'] == OrderStatus.DC_PENDING:
            reversal_order.status = OrderStatus.DC_PENDING
        elif reversal_order.status == OrderStatus.DC_PENDING and data['status'] == OrderStatus.REVERSAL_ORDER_PLACED:
            reversal_order.dc_number = data.get('dc_number')
            reversal_order.status = OrderStatus.REVERSAL_ORDER_PLACED
        elif reversal_order.status == OrderStatus.REVERSAL_ORDER_PLACED and data['status'] == OrderStatus.REVERSAL_ORDER_DELIVERED:
            reversal_order.status = OrderStatus.REVERSAL_ORDER_DELIVERED
            reversal_order.delivered_at = data.get('delivered_at')
        else:
            return {"status": "failed", "message": f"you order is already in {reversal_order.status} state "},400
        db.session.commit()
        return {"status": "success", "message": "Reversal order updated successfully!"},200

    @staticmethod
    def get_reversal_orders(status=None,user_contact_number=None):
        query = ReversalOrder.query
        if user_contact_number:
            query = query.filter(ReversalOrder.user_contact_number == user_contact_number)
        elif status==OrderStatus.REVERSAL_REVIEW_PENDING:
            query = query.filter(ReversalOrder.status == status)
        elif status == OrderStatus.DC_PENDING:
            query = query.filter(ReversalOrder.status == status)
        elif status == OrderStatus.REVERSAL_ORDER_PLACED:
            query = query.filter(ReversalOrder.status == status)
        elif status == OrderStatus.REVERSAL_ORDER_DELIVERED:
            query = query.filter(ReversalOrder.status == status)

        return query.all()

    @staticmethod
    def delete_reversal_order(reversal_order_id):
        reversal_order = ReversalOrder.query.get(reversal_order_id)
        if not reversal_order:
            return {"status": "fail", "message": "Reversal order not found!"}
        db.session.delete(reversal_order)
        db.session.commit()
        return {"status": "success", "message": "Reversal order deleted successfully!"}
