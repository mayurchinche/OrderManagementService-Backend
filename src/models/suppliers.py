from src.db.db import db


class Suppliers(db.Model):
    __tablename__ = "suppliers"
    supplier_name = db.Column(db.String(100), primary_key=True,unique=True, nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)


    def __repr__(self):
        return f"<Suppliers {self.supplier_name}: {self.contact_number}>"