import traceback

from flask import jsonify
from sqlalchemy import text, inspect

from src.db.db import db
from src.models.order_details import OrderDetails


def add_order(data):
    try:
        new_order = OrderDetails(
            user_contact_number=data["user_contact_number"],
            name_of_customer=data["name_of_customer"],
            materials=data["materials"],
            model=data["model"],  # Make sure 'model' is also included in the properties
            ordered_quantity=data["ordered_quantity"],
            order_to=data["order_to"],
            order_date=data.get(
                "order_date"
            ),  # Using get to avoid KeyError if not provided
            received_date=data.get(
                "received_date"
            ),  # Using get to avoid KeyError if not provided
            pending_quantity=data["pending_quantity"],
        )

        db.session.add(new_order)
        db.session.commit()
        return (
            jsonify(
                {"message": "Order added successfully!", "order_id": new_order.order_id}
            ),
            201,
        )
    except Exception as ex:
        print("Adding new oder failed! ", {traceback.print_exc()})
        return (
            jsonify(
                {"message": "Adding new oder failed!", "order_id": new_order.order_id}
            ),
            500,
        )


def get_orders_by_user(contact_number):
    try:
        orders = OrderDetails.query.filter_by(user_contact_number=contact_number).all()

        # Convert result into a list of dictionaries
        order_list = [
            {
                column.name: getattr(order, column.name, None)
                for column in order.__table__.columns
            }
            for order in orders
        ]

        # orders = OrderDetails.query.filter_by(user_contact_number=contact_number).all()
        return jsonify(order_list), 200
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
        print("column_name", "column_type")
        sql = f"ALTER TABLE order_details ADD COLUMN {column_name} VARCHAR(255)"
        print(sql)
        db.session.execute(text(sql))
        db.session.commit()
        return jsonify({"message": f"Column {column_name} added successfully!"}), 200

    except Exception as ex:
        print("Adding new oder failed! ", {traceback.print_exc()})
        return jsonify({"message": "Unable to fetch the orders!"}), 500


def update_order(order_id, order_status, pending_quantity):
    # Fetch the order by ID
    # Fetch the order by ID
    order = OrderDetails.query.get(order_id)
    print("order", order)
    if not order:
        return jsonify({"error": "Order not found."}), 404

    # Update the order status and/or pending quantity
    print("order_status", order_status)
    if order_status:
        order.order_status = order_status
    print(order)
    if pending_quantity is not None:
        order.pending_quantity = pending_quantity

    print(order)
    db.session.commit()

    return (
        jsonify({"message": "Order updated successfully!", "order_id": order_id}),
        201,
    )


def add_dynamic_order(data):
    # Reflect the latest metadata to capture newly added columns
    db.metadata.reflect(bind=db.engine, only=[OrderDetails.__tablename__])

    db.metadata.reflect(bind=db.engine, only=[OrderDetails.__tablename__])

    # Handle known fields using ORM
    static_order_data = {
        "user_contact_number": data["user_contact_number"],
        "name_of_customer": data["name_of_customer"],
        "materials": data["materials"],
        "model": data["model"],
        "ordered_quantity": data["ordered_quantity"],
        "order_to": data["order_to"],
        "order_date": data.get("order_date"),
        "received_date": data.get("received_date"),
        "pending_quantity": data["pending_quantity"],
    }

    # Create the ORM object for known fields
    new_order = OrderDetails(**static_order_data)
    db.session.add(new_order)
    db.session.commit()  # Commit ORM fields first to get the order ID

    # Handle additional dynamic columns using raw SQL
    dynamic_order_data = {}
    inspector = inspect(db.engine)

    # Get all columns for the order_details table
    order_details_columns = [
        column["name"] for column in inspector.get_columns("order_details")
    ]

    for column in order_details_columns:
        print(column)
        if column in data.keys() and column not in static_order_data.keys():
            print("Is in dynamic")
            dynamic_order_data[column] = data[column]

    if dynamic_order_data:
        # Generate the update query for dynamic columns
        set_clause = ", ".join([f"{key} = :{key}" for key in dynamic_order_data.keys()])
        query = f"UPDATE {OrderDetails.__tablename__} SET {set_clause} WHERE order_id = :order_id"
        dynamic_order_data["order_id"] = new_order.order_id

        # Execute raw SQL to update dynamic columns
        print(query)
        db.session.execute(text(query), dynamic_order_data)
        db.session.commit()
    return (
        jsonify(
            {"message": "Order added successfully", "order_id": new_order.order_id}
        ),
        201,
    )
