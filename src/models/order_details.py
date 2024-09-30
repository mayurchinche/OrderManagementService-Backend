from datetime import datetime

from src.db.db import  db

class OrderDetails(db.Model):
    __tablename__ = 'order_details'

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_name = db.Column(db.Integer, db.ForeignKey('users.contact_number'), nullable=False)

    name_of_customer= db.Column(db.String(100), nullable=False)
    po_no_or_whatsapp_date=db.Column(db.DateTime, default=datetime.utcnow)
    materials=db.Column(db.String(100), nullable=False)
    model=db.Column(db.String(100), nullable=False)
    odered_quantity=db.Column(db.Integer, nullable=False)
    order_to=db.Column(db.String(100), nullable=False)
    order_date=db.Column(db.DateTime, default=datetime.utcnow)
    received_date=db.Column(db.DateTime, default=datetime.utcnow)
    pending_quantity=db.Column(db.Integer, nullable=False)

    # Define relationship with the users table
    user = db.relationship('Users', backref=db.backref('order_details', lazy=True))

    def __repr__(self):
        return f'<Order {self.order_id} for User {self.user_name}>'