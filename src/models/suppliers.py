from src.db.db import db


class Suppliers(db.Model):
    __tablename__ = "suppliers"



    supplier_id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    response_time = db.Column(db.Integer)  # Days taken to respond to orders
    delivery_accuracy = db.Column(db.Float)  # Percentage of successful deliveries

    def __repr__(self):
        return f"<Suppliers {self.supplier_id}: {self.supplier_name}>"