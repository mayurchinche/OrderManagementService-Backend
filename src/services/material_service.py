# src/services/material_service.py
from flask import jsonify

from src.models.materials import Materials
from src.db.db import db
from src.models.materials import Materials
from src.db.db import db

class MaterialService:
    @staticmethod
    def get_all_materials():
        materials = Materials.query.all()
        return jsonify([{"material_name": mat.material_name, "description": mat.description} for mat in materials],200)

    @staticmethod
    def add_material(material_name, description):
        existing_material = Materials.query.filter_by(material_name=material_name).first()
        if existing_material:
            return jsonify({"status": "failed", "message": "Material already exists!"}, 400)

        new_material = Materials(material_name=material_name, description=description)
        db.session.add(new_material)
        db.session.commit()
        return jsonify({"status": "success", "message": "Material added successfully!"}, 201)

    @staticmethod
    def delete_material(material_name):
        material = Materials.query.filter_by(material_name=material_name).first()
        if not material:
            return jsonify({"status": "fail", "message": "Material not found!"}, 404)

        db.session.delete(material)
        db.session.commit()
        return jsonify({"status": "success", "message": "Material deleted successfully!"}, 200)
