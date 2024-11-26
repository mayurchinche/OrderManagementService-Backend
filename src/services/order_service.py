import traceback
from datetime import datetime

from sqlalchemy.sql import text
from flask import jsonify
from gunicorn.config import PrintConfig
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
            if not start_date or not end_date:
                return jsonify({"error": "start_date and end_date are required"},400)

            result = (db.session.query(
                func.sum(OrderDetails.expected_price).label('total_expected'),
                func.sum(OrderDetails.ordered_price).label('total_ordered')
            ).filter(OrderDetails.order_date.between(start_date, end_date),OrderDetails.status == OrderStatus.ORDER_DELIVERED).one())
            return jsonify({"total_expected": result.total_expected or 0, "total_ordered": result.total_ordered or 0},200)
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "fail", "message": str(e)}, 500)

    @staticmethod
    def get_avg_of_expected_price_and_avg_of_ordered_price(start_date, end_date,interval):
        try:
            if not start_date or not end_date:
                return jsonify({"error": "start_date and end_date are required"},400)

            # Define the SQL function for grouping
            if interval == 'daily':
                group_by_func = "DATE(order_date)"
            elif interval == 'monthly':
                group_by_func = "DATE_FORMAT(order_date, '%Y-%m')"
            else:
                return jsonify({"error": "Invalid interval"},400)

            # Raw SQL query
            query = text(f"""
                SELECT 
                    {group_by_func} AS time_period,
                    AVG(expected_price) AS average_expected_price,
                    AVG(ordered_price) AS average_ordered_price
                FROM 
                    order_details
                WHERE 
                    status = 'Order_Delivered' 
                    AND DATE(order_date) BETWEEN :start_date AND :end_date
                GROUP BY 
                    time_period
                ORDER BY 
                    time_period;
            """)

            # Execute the query
            # Convert to YYYY-MM-DD format
            start_date = datetime.strptime(start_date, "%d-%m-%Y").strftime("%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%d-%m-%Y").strftime("%Y-%m-%d")
            results = db.session.execute(query, {"start_date": start_date, "end_date": end_date}).fetchall()
            # Format response
            trend = [
                {
                    "time_period": row.time_period,
                    "average_expected_price": row.average_expected_price,
                    "average_ordered_price": row.average_ordered_price
                }
                for row in results
            ]

            return jsonify({"trend": trend})
        except Exception as e:
            print(traceback.print_exc())
            db.session.rollback()
            return jsonify({"status": "fail", "message": str(e)}, 500)


    @staticmethod
    def get_supplier_performance(start_date, end_date):
        try:
            if not start_date or not end_date:
                return jsonify({"error": "start_date and end_date are required"},400)

            # Convert date formats to YYYY-MM-DD
            try:
                start_date = datetime.strptime(start_date, "%d-%m-%Y").strftime("%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%d-%m-%Y").strftime("%Y-%m-%d")
            except ValueError:
                return jsonify({"error": "Invalid date format. Use DD-MM-YYYY"},400)

            # Query for average orders delivered by each supplier
            query_avg_orders = text("""
                SELECT 
                    supplier_name,
                    COUNT(*) AS total_orders,
                    ROUND(COUNT(*) / NULLIF(DATEDIFF(:end_date, :start_date), 0), 2) AS average_orders_per_day
                FROM 
                    order_details
                WHERE 
                    status = 'Order_Delivered'
                    AND DATE(STR_TO_DATE(order_date, '%Y-%m-%d')) BETWEEN :start_date AND :end_date
                GROUP BY 
                    supplier_name
                ORDER BY 
                    total_orders DESC;
            """)
            # Query for average delivery time by each supplier
            query_avg_delivery_time = text("""
                SELECT 
                    supplier_name,
                    AVG(DATEDIFF(STR_TO_DATE(order_date, '%Y-%m-%d'), STR_TO_DATE(received_date, '%Y-%m-%d'))) AS avg_delivery_days
                FROM 
                    order_details
                WHERE 
                    status = 'Order_Delivered'
                    AND DATE(STR_TO_DATE(order_date, '%Y-%m-%d')) BETWEEN :start_date AND :end_date
                GROUP BY 
                    supplier_name
                ORDER BY 
                    avg_delivery_days ASC;
            """)


            query_monthly_avg_orders = text("""
                SELECT 
                    supplier_name,
                    DATE_FORMAT(DATE(STR_TO_DATE(order_date, '%Y-%m-%d')), '%Y-%m') AS month,
                    COUNT(*) AS total_orders_in_month,
                    ROUND(AVG(COUNT(*)) OVER (PARTITION BY supplier_name), 2) AS average_orders_per_month
                FROM 
                    order_details
                WHERE 
                    status = 'Order_Delivered'
                    AND DATE(STR_TO_DATE(order_date, '%Y-%m-%d')) BETWEEN :start_date AND :end_date
                GROUP BY 
                    supplier_name, month
                ORDER BY 
                    supplier_name, month;
            """)

            # Execute the queries
            avg_orders_results = db.session.execute(query_avg_orders,
                                                    {"start_date": start_date, "end_date": end_date}).fetchall()
            avg_delivery_time_results = db.session.execute(query_avg_delivery_time,
                                                           {"start_date": start_date, "end_date": end_date}).fetchall()

            monhtly_avg_query_results = db.session.execute(
                query_monthly_avg_orders,
                {"start_date": start_date, "end_date": end_date}
            )

            monthly_avg_data = [
                {
                    "supplier_name": row.supplier_name,
                    "month": row.month,
                    "total_orders_in_month": row.total_orders_in_month,
                    "average_orders_per_month": row.average_orders_per_month
                }
                for row in monhtly_avg_query_results
            ]

            # Format the results
            avg_orders_data = [
                {
                    "supplier_name": row.supplier_name,
                    "total_orders": row.total_orders,
                    "average_orders_per_day": row.average_orders_per_day
                }
                for row in avg_orders_results
            ]

            avg_delivery_time_data = [
                {
                    "supplier_name": row.supplier_name,
                    "avg_delivery_days": row.avg_delivery_days
                }
                for row in avg_delivery_time_results
            ]

            # Combine results into response
            response = {
                "average_orders_by_supplier": avg_orders_data,
                "average_delivery_time_by_supplier": avg_delivery_time_data,
                "monthly_orders_by_supplier": monthly_avg_data
            }

            return jsonify(response)
        except Exception as ex:
            db.session.rollback()
            return jsonify({"status": "fail", "message": str(ex)}, 500)





