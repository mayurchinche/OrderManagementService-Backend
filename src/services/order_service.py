from src.constants.order_status import OrderStatus
from src.db.db import db
from src.models.order_details import OrderDetails

class OrderService:
    @staticmethod
    def get_orders(status=None, contact_number=None, limit=None, offset=None):
        query = OrderDetails.query
        if status and contact_number:
            query = query.filter(OrderDetails.status == status, OrderDetails.user_contact_number == contact_number)
        elif status:
            query = query.filter(OrderDetails.status == status)
        elif contact_number:
            query = query.filter(OrderDetails.user_contact_number == contact_number)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        return query.all()
    @staticmethod
    def add_order(data):
        material_name = data['material_name'],
        order_date = data['order_date']
        order_quantity = data['order_quantity']
        ordered_by = data['ordered_by']
        user_contact_number = data['user_contact_number']
        new_order = OrderDetails(
            material_name=material_name,
            order_date=order_date,
            order_quantity=order_quantity,
            ordered_by=ordered_by,
            user_contact_number=user_contact_number
        )
        db.session.add(new_order)
        db.session.commit()
        return {"status": "success", "message": "Order added successfully!"}

    @staticmethod
    def update_order(order_id, data=None, status=None):
        order = OrderDetails.query.get(order_id)
        print("data",data)
        print("status",status)
        if not order:
            return {"status": "fail", "message": "Order not found!"}
        if not status:
            status = order.status
        # Review done move order to PO_PENDING
        if order.status == OrderStatus.REVIEW_PENDING and data:
            order.expected_price = data.get("expected_price")
            order.approved_by = data.get("approved_by")
            order.order_quantity = data.get("order_quantity")
            order.status = OrderStatus.PO_PENDING

        # PO_PENDING move to PO_RAISED
        elif order.status == OrderStatus.PO_PENDING and data:
            print("Is in if")
            order.po_no = data.get("po_no")
            order.supplier_name = data.get("supplier_name")
            order.ordered_price = data.get("ordered_price")
            order.po_raised_by = data.get("po_raised_by")
            order.status=OrderStatus.ORDER_PLACED

        # PO_RAISED move to DELIVERED
        elif order.status == OrderStatus.ORDER_PLACED:
            print("Is in elif")
            order.received_date =data.get("received_date")
            order.status = status
        else:
            var = {"status": "Failed", "message": f"Order is already in {order.status}!"}
            return var
        print(order.order_id, order.status)
        db.session.commit()
        return {"status": "success", "message": "Order updated successfully!"}

    @staticmethod
    def delete_order(order_id):
        order = OrderDetails.query.get(order_id)
        if not order:
            return {"status": "fail", "message": "Order not found!"}

        db.session.delete(order)
        db.session.commit()
        return {"status": "success", "message": "Order deleted successfully!"}

    @staticmethod
    def get_review_pending_orders():
        try:
            # Query to get all orders with Review_Pending status
            review_pending_orders = OrderDetails.query.filter_by(status=OrderStatus.REVIEW_PENDING).all()
            return [order.to_dict() for order in review_pending_orders]  # Assume `to_dict` is implemented in your model
        except Exception as e:
            raise Exception(f"Error fetching review pending orders: {str(e)}")

    @staticmethod
    def approve_order(order_id, data):
        try:
            order = OrderDetails.query.filter_by(order_id=order_id).first()
            if not order:
                return {"status": "fail", "message": "Order not found!"}, 404

            # Update order details with data from request
            order.order_quantity = data.get("order_quantity", order.order_quantity)
            order.expected_price = data.get("expected_price", order.expected_price)
            order.approved_by = data.get("approved_by", order.approved_by)
            order.status = OrderStatus.PO_PENDING  # Update the status to Approved

            # Commit changes to the database
            db.session.commit()
            return {"status": "success", "message": "Order approved successfully!"}, 200
        except Exception as e:
            db.session.rollback()
            return {"status": "fail", "message": str(e)}, 500