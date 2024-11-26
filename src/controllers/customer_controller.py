# src/controllers/customer_controller.py
from flask import jsonify, request
from numpy.f2py.auxfuncs import throw_error

from src.services.customer_service import CustomerService


class CustomerController:

    @staticmethod
    def get_all_customers():
        try:
            return CustomerService.get_all_customers()
        except Exception as e:
            return jsonify({"error": str(e)}, 500)

    @staticmethod
    def add_customer(data):
        try:
            customer_name = data.get("customer_name")
            description = data.get("description")
            return CustomerService.add_customer(customer_name,description)
        except Exception as e:
            return jsonify({"error": str(e)}, 500)

    @staticmethod
    def delete_customer(customer_name):
        try:
            return CustomerService.delete_customer(customer_name)
        except Exception as e:
            return jsonify({"error": str(e)}, 500)
