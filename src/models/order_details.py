from datetime import datetime
from email.policy import default

from src.db.db import db


class OrderDetails(db.Model):
    __tablename__ = "order_details"

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_contact_number = db.Column(
        db.String(15), db.ForeignKey("users.contact_number"), nullable=False
    )
    order_date = db.Column(db.String(100), nullable=False,default=datetime.today())
    name_of_customer = db.Column(db.String(100), nullable=False,default='None')
    po_no = db.Column(db.String(50), nullable=False, default='None')
    whatsapp_date = db.Column(db.String(100), nullable=True, default='None')
    material_name = db.Column(db.String(100), nullable=False, default='None')
    model = db.Column(db.String(100), nullable=False,default='None')
    order_quantity = db.Column(db.Integer, nullable=False,default=0)
    order_to = db.Column(db.String(100), nullable=False,default='None')
    received_date = db.Column(db.String(100), nullable=True,default='None')
    pending_quantity = db.Column(db.Integer, nullable=True,default=order_quantity)
    ordered_by = db.Column(db.String(50), nullable=False,default='None')
    approved_by = db.Column(db.String(50), nullable=True,default='None')
    po_raised_by = db.Column(db.String(50), nullable=True,default='None')
    status = db.Column(db.String(50), nullable=False,default='REVIEW_PENDING')
    note = db.Column(db.String(255), nullable=True,default='None')

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
        return f"<Order {self.order_id} for User {self.user_contact_number}>"

    def to_dict(self):
        """ Convert OrderDetails object to dictionary format """
        return {
            "order_id": self.order_id,
            "user_contact_number": self.user_contact_number,
            "order_date": self.order_date,
            "name_of_customer": self.name_of_customer,
            "po_no": self.po_no,
            "whatsapp_date": self.whatsapp_date,
            "material_name": self.material_name,
            "model": self.model,
            "order_quantity": self.order_quantity,
            "order_to": self.order_to,
            "received_date": self.received_date,
            "pending_quantity": self.pending_quantity,
            "ordered_by": self.ordered_by,
            "approved_by": self.approved_by,
            "po_raised_by": self.po_raised_by,
            "status": self.status,
            "note": self.note,
            "expected_price": self.expected_price,
            "ordered_price": self.ordered_price,
            "material_id": self.material_id,
            "supplier_id": self.supplier_id,
        }
