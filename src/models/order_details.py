from datetime import datetime

from src.db.db import db


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
    status = db.Column(db.String(50), nullable=False)
    note = db.Column(db.String(255), nullable=True)

    expected_price = db.Column(db.Float, nullable=True)  # Set by manager
    ordered_price = db.Column(db.Float, nullable=True)  # Final price by PO team

    material_id = db.Column(db.Integer, db.ForeignKey("materials.material_id"))
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.supplier_id"))

    # Define relationship with the users table
    user = db.relationship("User", backref=db.backref("orders", lazy=True))
    material = db.relationship(
        "Materials", backref="orders"
    )  # backref is useed for showing the relationship in readable format like material.orders
    supplier = db.relationship("Suppliers", backref="orders")

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
