from src.db.db import db


class Customers(db.Model):
    __tablename__ = "customers"
    customer_name = db.Column(db.String(255), primary_key=True,nullable=False, unique=True)
    description = db.Column(db.String(500))


    def __repr__(self):
        return f"<Customers {self.customer_name}: {self.description}>"