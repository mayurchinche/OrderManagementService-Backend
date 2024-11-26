from flask import request
from flask_restful import Resource, reqparse

from src.constants.roles import Roles
from src.controllers.customer_controller import CustomerController

from src.sequrity.decorators import apply_decorators


class CustomerResource(Resource):
    def __init__(self):
        self.controller = CustomerController()

    @staticmethod
    @apply_decorators()
    def get():
        """
        Get All Customers
        ---
        tags:
          - Customers
        responses:
          200:
            description: Successfully fetched all customers
          500:
            description: Error fetching customers
        """
        return CustomerController.get_all_customers()

    @staticmethod
    @apply_decorators(allowed_roles=Roles.ONLY_MANAGER)
    def post():
        """
        Add New Customer
        ---
        tags:
          - Customers
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - customer_name
                - description
              properties:
                customer_name:
                  type: string
                  description: Name of the customer
                description:
                  type: string
                  description: Description of the customer
        responses:
          201:
            description: Customer successfully added
          400:
            description: Customer already exists
          500:
            description: Error adding customer
        """
        # Extract data from request body
        data = request.get_json()
        # Call the controller to add customer
        return CustomerController.add_customer(data)

    @staticmethod
    @apply_decorators(allowed_roles=Roles.ONLY_MANAGER)
    def delete():
        """
        Delete Customer
        ---
        tags:
          - Customers
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - customer_name
              properties:
                customer_name:
                  type: string
                  description: name of the customer to delete
        responses:
          200:
            description: Customer successfully deleted
          404:
            description: Customer not found
          500:
            description: Error deleting customer
        """
        data = request.get_json()

        return CustomerController.delete_customer(data.get("customer_name"))
