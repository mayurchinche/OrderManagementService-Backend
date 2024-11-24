from flask import jsonify

from src.models.suppliers import Suppliers
from src.db.db import db

class SupplierService:
    @staticmethod
    def add_supplier(supplier_name, contact_number):
        print("Quring to DB")
        existing_supplier = Suppliers.query.filter_by(supplier_name=supplier_name).first()
        if existing_supplier:
            return jsonify({"status": "fail", "message": "Supplier already exists!"}, 400)
        print("Adding to DB")
        new_supplier = Suppliers(supplier_name=supplier_name, contact_number=contact_number)
        db.session.add(new_supplier)
        db.session.commit()
        print("Added to DB")
        return jsonify({"status": "success", "message": "Supplier added successfully!"}, 201)

    @staticmethod
    def get_all_suppliers():
        suppliers = Suppliers.query.all()
        return jsonify([{"supplier_name": sup.supplier_name, "contact_number": sup.contact_number} for
                sup in suppliers],200)
