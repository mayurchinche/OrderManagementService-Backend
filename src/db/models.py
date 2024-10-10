from datetime import datetime

from .db import db
from src.controllers.cost_effectiveness_controller import calculate_cost_effectiveness
from ..constants import OrderStatus


class Materials(db.Model):
    __tablename__ = "materials"

    material_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    material_name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(500))

    def __repr__(self):
        return f"<Material {self.material_id}: {self.material_name}>"


class Suppliers(db.Model):
    __tablename__ = "suppliers"

    supplier_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_name = db.Column(db.String(255), nullable=False, unique=True)
    contact_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(500))

    def __repr__(self):
        return f"<Supplier {self.supplier_id}: {self.supplier_name}>"


class OrderDetails(db.Model):
    __tablename__ = "order_details"

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_contact_number = db.Column(
        db.String(15), db.ForeignKey("users.contact_number"), nullable=False
    )

    order_date = db.Column(db.Date, nullable=False)
    name_of_customer = db.Column(db.String(100), nullable=False)
    po_no = db.Column(db.String(50), nullable=False)
    whatsapp_date = db.Column(db.Date, nullable=True)
    material_name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    order_quantity = db.Column(db.Integer, nullable=False)
    order_to = db.Column(db.String(100), nullable=False)
    received_date = db.Column(db.Date, nullable=True)
    pending_quantity = db.Column(db.Integer, nullable=True)
    ordered_by = db.Column(db.String(50), nullable=False)
    approved_by = db.Column(db.String(50), nullable=True)
    po_raised_by = db.Column(db.String(50), nullable=True)
    status = db.Column(
        db.String(50), nullable=False, default=OrderStatus.REVIEW_PENDING
    )  # Default status
    note = db.Column(db.String(255), nullable=True)

    material_id = db.Column(db.Integer, db.ForeignKey("materials.material_id"))
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.supplier_id"))

    material_id = db.Column(db.Integer, db.ForeignKey("materials.material_id"))
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.supplier_id"))

    # Define relationship with the users table
    user = db.relationship("User", backref=db.backref("orders", lazy=True))
    material = db.relationship(
        "Materials", backref="orders"
    )  # backref is useed for showing the relationship in readable format like material.orders
    supplier = db.relationship("Suppliers", backref="orders")

    def update_status(self, new_status):
        self.status = new_status
        db.session.commit()

    def calculate_cost_effectiveness(self):
        return calculate_cost_effectiveness(self)

    def __repr__(self):
        return (
            f"<Order {self.order_id} for User {self.user_contact_number}, "
            f"Customer: {self.name_of_customer}, "
            f"Ordered Quantity: {self.ordered_quantity}, "
            f"Materials: {self.materials}, "
            f"Order To: {self.order_to}, "
            f"Order Date: {self.order_date}, "
            f"Pending Quantity: {self.pending_quantity}>"
        )


class ReversalOrder(db.Model):
    __tablename__ = "reversal_orders"

    reversal_order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_order_id = db.Column(
        db.Integer, db.ForeignKey("order_details.order_id"), nullable=False
    )
    user_contact_number = db.Column(
        db.String(15), db.ForeignKey("users.contact_number"), nullable=False
    )
    name_of_customer = db.Column(db.String(100), nullable=False)
    materials = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    ordered_quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    pending_quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(
        db.String(50), nullable=False, default=OrderStatus.REVIEW_PENDING
    )  # Default status
    # Define relationship with the original order
    original_order = db.relationship("OrderDetails", backref="reversal_orders")

    def __repr__(self):
        return (
            f"<ReversalOrder {self.reversal_id} for Order {self.original_order_id}, "
            f"Faulty Quantity: {self.faulty_quantity}, "
            f"Reason: {self.reversal_reason}>"
        )
