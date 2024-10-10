from flask import Blueprint, request, jsonify
from src.models.suppliers import Suppliers
from src.db.db import db

supplier_bp = Blueprint("suppliers", __name__)


@supplier_bp.route("/suppliers", methods=["POST"])
def add_supplier():
    data = request.get_json()
    new_supplier = Suppliers(name=data["name"], contact_info=data.get("contact_info"))
    db.session.add(new_supplier)
    db.session.commit()
    return jsonify({"message": "Supplier added successfully!"}), 201


@supplier_bp.route("/suppliers", methods=["GET"])
def get_suppliers():
    suppliers = Suppliers.query.all()
    return jsonify(
        [
            {
                "id": supplier.id,
                "name": supplier.name,
                "contact_info": supplier.contact_info,
            }
            for supplier in suppliers
        ]
    )
