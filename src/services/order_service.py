from ..db.models import OrderDetails


def create_order(data):
    """
    Create a new order
            ---
            tags:
              - Orders
            parameters:
              - in: body
                name: body
                schema:
                  type: object
                  required:
                    - user_contact_number
                    - material_id
                    - quantity
                  properties:
                    user_contact_number:
                      type: string
                      description: The user's contact number placing the order
                    material_id:
                      type: integer
                      description: The material ID being ordered
                    quantity:
                      type: integer
                      description: Quantity of the material to be ordered
            responses:
              201:
                description: Order created successfully!
              400:
                description: Invalid input. Please check your request.
              401:
                description: Unauthorized, JWT token is invalid or missing.
              500:
                description: Server error occurred while creating the order.
    """

    pass


from src.models.order_details import OrderDetails
from src.db.db import db


class OrderService:
    @staticmethod
    def update_order_status(order_id, new_status):
        order = OrderDetails.query.get(order_id)
        if order:
            order.order_status = new_status
            db.session.commit()
            return order
        return None

    @staticmethod
    def create_reversal_order(original_order_id, faulty_quantity):
        original_order = OrderDetails.query.get(original_order_id)
        if original_order:
            reversal_order = OrderDetails(
                user_contact_number=original_order.user_contact_number,
                name_of_customer=original_order.name_of_customer,
                materials=original_order.materials,
                model=original_order.model,
                ordered_quantity=faulty_quantity,
                order_to=original_order.order_to,
                order_status="Reversal_Order_Placed",
                reversal_status="Pending"
                # Include other necessary fields
            )
            db.session.add(reversal_order)
            db.session.commit()
            return reversal_order
        return None
