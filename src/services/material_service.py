# src/services/material_service.py
from flask import jsonify

from src.models.materials import Materials
from src.db.db import db


class MaterialService:

    @staticmethod
    def get_all_materials():
        materials = Materials.query.all()
        return [{"material_id": m.material_id, "material_name": m.material_name, "description": m.description} for m in
                materials]

    @staticmethod
    def add_material(data):
        material_name = data.get("material_name")
        description = data.get("description", "")

        if not material_name:
            raise ValueError("Material name is required")

        new_material = Materials(material_name=material_name, description=description)
        db.session.add(new_material)
        db.session.commit()
        return {"material_id": new_material.material_id, "material_name": new_material.material_name,
                "description": new_material.description}

    @staticmethod
    def delete_material(material_id):
        material = Materials.query.get(material_id)
        if material:
            db.session.delete(material)
            db.session.commit()
            return True
        return False


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
    def delete_material(material_nmae):
        material = Materials.query.filter_by(material_nmae=material_nmae).first()
        if not material:
            return jsonify({"status": "fail", "message": "Material not found!"}, 404)

        db.session.delete(material)
        db.session.commit()
        return jsonify({"status": "success", "message": "Material deleted successfully!"}, 200)
