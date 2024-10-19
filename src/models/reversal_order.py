from datetime import datetime


from src.constants.order_status import OrderStatus
from src.db.db import db

class ReversalOrder(db.Model):
    __tablename__ = "reversal_order"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_order_id = db.Column(db.Integer, db.ForeignKey("order_details.order_id"))
    original_order_material_name = db.Column(db.String(100), nullable=True)
    origin_order_supplier_name = db.Column(db.String(100), nullable=True)
    original_order_quantity = db.Column(db.Integer, nullable=True)
    user_contact_number = db.Column(db.String(100), nullable=True,index=True)
    reversal_quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.String(100), nullable=True, default=datetime.today())
    description = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), nullable=False, default=OrderStatus.REVERSAL_REVIEW_PENDING,index=True)
    dc_number = db.Column(db.String(50), nullable=True)
    delivery_date = db.Column(db.String(100), nullable=True, default='None')
    # Relationship to link to the original order
    original_order = db.relationship("OrderDetails", backref="reversals")

    __table_args__ = (
        db.Index('idx_reversal_order_status', 'status'),
        db.Index('idx_user_contact_number', 'user_contact_number'),
    )

    def __repr__(self):
        return f"<Reversal Order {self.id} linked to Order {self.original_order_id}>"

    def to_dict(self):
        """ Convert ReversalOrder object to dictionary format """
        return {
            "id": self.id,
            "original_order_id": self.original_order_id,
            "original_order_material_name": self.original_order_material_name,
            "origin_order_supplier_name": self.origin_order_supplier_name,
            "original_order_quantity": self.original_order_quantity,
            "user_contact_number": self.user_contact_number,
            "reversal_quantity": self.reversal_quantity,
            "created_at": self.created_at,  # Format datetime for JSON serialization
            "description": self.description,
            "status": self.status,
            "dc_number": self.dc_number
        }
