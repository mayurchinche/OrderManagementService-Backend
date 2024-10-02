import traceback

from flask import jsonify
from sqlalchemy import text

from src.db.db import db
from src.models.order_details import OrderDetails


def add_order(data):
    try:
        new_order = OrderDetails(
            user_contact_number=data['user_contact_number'],
            name_of_customer=data['name_of_customer'],
            materials=data['materials'],
            model=data['model'],  # Make sure 'model' is also included in the properties
            ordered_quantity=data['ordered_quantity'],
            order_to=data['order_to'],
            order_date=data.get('order_date'),  # Using get to avoid KeyError if not provided
            received_date=data.get('received_date'),  # Using get to avoid KeyError if not provided
            pending_quantity=data['pending_quantity']
        )

        db.session.add(new_order)
        db.session.commit()
        return jsonify({"message": "Order added successfully!", "order_id": new_order.order_id}), 201
    except Exception as ex:
        print("Adding new oder failed! ",{traceback.print_exc()})
        return jsonify({"message": "Adding new oder failed!", "order_id": new_order.order_id}), 500

def get_orders_by_user(contact_number):
    try:
        orders = OrderDetails.query.filter_by(user_contact_number=contact_number).all()
        return jsonify([order.__repr__() for order in orders]), 200
    except Exception as ex:
        print("Adding new oder failed! ", {traceback.print_exc()})
        return jsonify({"message": "Unable to fetch the orders!"}), 500

def show_all_orders():
    try:

        orders = OrderDetails.query.all()
        print("type", type(orders))
        print("order details", orders[0])
        return jsonify([order.__repr__() for order in orders]), 200
    except Exception as ex:
        print("Adding new oder failed! ", {traceback.print_exc()})
        return jsonify({"message": "Unable to fetch the orders!"}), 500

def add_new_column(column_name):
    try:
        print("column_name","column_type" )
        sql = f"ALTER TABLE order_details ADD COLUMN {column_name} VARCHAR(255)"
        print(sql)
        db.session.execute(text(sql))
        db.session.commit()
        return jsonify({"message": f"Column {column_name} added successfully!"}), 200

    except Exception as ex:
        print("Adding new oder failed! ", {traceback.print_exc()})
        return jsonify({"message": "Unable to fetch the orders!"}), 500