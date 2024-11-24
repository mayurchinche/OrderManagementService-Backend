from flask import jsonify
from sqlalchemy import func

from src.constants.order_status import OrderStatus
from src.db.db import db
from src.models.order_details import OrderDetails

class OrderService:
    @staticmethod
    def get_orders(status=None, contact_number=None, limit=None, offset=None):
        query = OrderDetails.query

        if isinstance(status, (tuple, list)):
            # Apply the filter using the .in_ method to match any of the statuses
            query = query.filter(OrderDetails.status.in_(status))
        elif status and contact_number:
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
        model= data['model']
        customer_name = data['customer_name']
        new_order = OrderDetails(
            material_name=material_name,
            order_date=order_date,
            order_quantity=order_quantity,
            ordered_by=ordered_by,
            user_contact_number=user_contact_number,
            model=model,
            name_of_customer=customer_name
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify({"status": "success", "message": "Order added successfully!"},200)

    @staticmethod
    def update_order(order_id, data=None, status=None):
        order = OrderDetails.query.get(order_id)
        if not order:
            return {"status": "fail", "message": "Order not found!"}
        if not status:
            status = order.status
        # Review done move order to PO_PENDING
        if order.status == OrderStatus.REVIEW_PENDING and data["status"]==OrderStatus.PO_PENDING:
            order.expected_price = data.get("expected_price")
            order.approved_by = data.get("approved_by")
            order.order_quantity = data.get("order_quantity")
            order.status = OrderStatus.PO_PENDING

        # PO_PENDING move to PO_RAISED
        elif order.status == OrderStatus.PO_PENDING and data["status"]==OrderStatus.ORDER_PLACED:
            order.po_no = data.get("po_no")
            order.supplier_name = data.get("supplier_name")
            order.ordered_price = data.get("ordered_price")
            order.po_raised_by = data.get("po_raised_by")
            order.status=OrderStatus.ORDER_PLACED

        # PO_RAISED move to DELIVERED
        elif (order.status == OrderStatus.ORDER_PLACED and data["status"]==OrderStatus.ORDER_DELIVERED) or (order.status == OrderStatus.PARTIALLY_DELIVERED and data["status"]==OrderStatus.ORDER_DELIVERED):
            order.received_date =data.get("received_date")
            received_quantity = data.get("received_quantity")
            pending_quantity = order.pending_quantity
            if pending_quantity == received_quantity:
                order.pending_quantity = pending_quantity - received_quantity
                order.status = OrderStatus.ORDER_DELIVERED
            else:
                order.pending_quantity = order.pending_quantity - received_quantity
                order.status = OrderStatus.PARTIALLY_DELIVERED
        else:
            var = jsonify({"status": "Failed", "message": f"Order is already in {order.status}!"},400)
            return var
        db.session.commit()
        return jsonify({"status": "success", "message": "Order updated successfully!"},200)

    @staticmethod
    def delete_order(order_id):
        order = OrderDetails.query.get(order_id)
        if not order:
            return jsonify({"status": "fail", "message": "Order not found!"}, 404)

        db.session.delete(order)
        db.session.commit()
        return jsonify({"status": "success", "message": "Order deleted successfully!"}, 200)

    @staticmethod
    def get_review_pending_orders():
        try:
            # Query to get all orders with Review_Pending status
            review_pending_orders = OrderDetails.query.filter_by(status=OrderStatus.REVIEW_PENDING).all()
            return jsonify([order.to_dict() for order in review_pending_orders],200)  # Assume `to_dict` is implemented in your model
        except Exception as e:
            raise jsonify({"status": "fail", "message": f"Error fetching review pending orders: {str(e)}"}, 500)

    @staticmethod
    def approve_order(order_id, data):
        try:
            order = OrderDetails.query.filter_by(order_id=order_id).first()
            if not order:
                return jsonify({"status": "fail", "message": "Order not found!"}, 404)

            # Update order details with data from request
            order.order_quantity = data.get("order_quantity", order.order_quantity)
            order.pending_quantity = order.order_quantity
            order.expected_price = data.get("expected_price", order.expected_price)
            order.approved_by = data.get("approved_by", order.approved_by)
            order.status = OrderStatus.PO_PENDING  # Update the status to Approved

            # Commit changes to the database
            db.session.commit()
            return jsonify({"status": "success", "message": "Order approved successfully!"}, 200)
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "fail", "message": str(e)}, 500)

    @staticmethod
    def get_sum_of_expected_price_and_sum_of_ordered_price(start_date,end_date):
        try:
            result = db.session.query(
                func.sum(OrderDetails.expected_price).label('total_expected'),
                func.sum(OrderDetails.ordered_price).label('total_ordered')
            ).filter(
                OrderDetails.status == OrderStatus.ORDER_DELIVERED,  # Only consider delivered orders
                OrderDetails.received_date.between(start_date, end_date)
            ).one()
            return jsonify({"total_expected": result.total_expected or 0, "total_ordered": result.total_actual or 0},200)
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "fail", "message": str(e)}, 500)