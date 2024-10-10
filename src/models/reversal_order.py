from datetime import datetime

from src.db.db import db


class ReversalOrder(db.Model):
    __tablename__ = "reversal_order"

    id = db.Column(db.Integer, primary_key=True)
    original_order_id = db.Column(db.Integer, db.ForeignKey("order_details.order_id"))
    faulty_quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Reversal_Pending")
    dc_status = db.Column(db.String(50), nullable=True)  # Delivery Challan status

    # Relationship to link to the original order
    original_order = db.relationship("OrderDetails", backref="reversals")
