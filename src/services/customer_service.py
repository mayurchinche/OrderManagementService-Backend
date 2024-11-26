# src/services/customer_service.py
from flask import jsonify

from src.models.customers import Customers

from src.db.db import db


class CustomerService:
    @staticmethod
    def get_all_customers():
        customers = Customers.query.all()
        return jsonify([{"customer_name": cust.customer_name, "description": cust.description} for cust in customers],
                       200)

    @staticmethod
    def add_customer(customer_name, description):
        existing_customer = Customers.query.filter_by(customer_name=customer_name).first()
        if existing_customer:
            return jsonify({"status": "failed", "message": "Customer already exists!"}, 400)

        new_customer = Customers(customer_name=customer_name, description=description)
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({"status": "success", "message": "Customer added successfully!"}, 201)

    @staticmethod
    def delete_customer(customer_name):
        customer = Customers.query.filter_by(customer_name=customer_name).first()
        if not customer:
            return jsonify({"status": "fail", "message": "Customer not found!"}, 404)

        db.session.delete(customer)
        db.session.commit()
        return jsonify({"status": "success", "message": "Customer deleted successfully!"}, 200)
