from datetime import datetime

from src.db.db import  db

class OrderDetails(db.Model):
    __tablename__ = 'order_details'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_contact_number = db.Column(db.String(15), db.ForeignKey('users.contact_number'), nullable=False)

    name_of_customer = db.Column(db.String(100), nullable=False)
    po_no_or_whatsapp_date = db.Column(db.DateTime, default=datetime.utcnow)
    materials = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    ordered_quantity = db.Column(db.Integer, nullable=False)
    order_to = db.Column(db.String(100), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    received_date = db.Column(db.DateTime, default=datetime.utcnow)
    pending_quantity = db.Column(db.Integer, nullable=False)

    # Define relationship with the users table
    user = db.relationship('User', backref=db.backref('OrderDetails', lazy=True))

    def __repr__(self):

        return (f"<Order {self.order_id} for User {self.user_contact_number}, "
                f"Customer: {self.name_of_customer}, "
                f"Ordered Quantity: {self.ordered_quantity}, "
                f"Materials: {self.materials}, "
                f"Order To: {self.order_to}, "
                f"Order Date: {self.order_date}, "
                f"Pending Quantity: {self.pending_quantity}>")