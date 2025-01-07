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
        return jsonify(
            [{"material_name": mat.material_name, "material_code": mat.material_code, "description": mat.description}
             for mat in materials], 200)

    @staticmethod
    def add_material(material_name, description, product_shortcut):
        # Find the highest existing material code with the given product shortcut
        last_material = (Materials.query
                         .filter(Materials.material_code.startswith(product_shortcut))
                         .order_by(Materials.material_code.desc())
                         .first())

        # Determine the next code number
        if last_material:
            last_number = int(last_material.material_code[len(product_shortcut):])
            next_number = last_number + 1
        else:
            next_number = 1

        # Generate the new material code
        material_code = f"{product_shortcut}{str(next_number).zfill(2)}"

        # Check if material with the same name already exists
        existing_material = Materials.query.filter_by(material_name=material_name).first()
        if existing_material:
            return jsonify({"status": "failed", "message": "Material already exists!"}, 400)

        # Add the new material with generated code
        new_material = Materials(material_name=material_name, description=description, material_code=material_code)
        db.session.add(new_material)
        db.session.commit()
        return jsonify({"status": "success", "message": "Material added successfully!", "material_code": material_code},
                       201)

    @staticmethod
    def delete_material(material_name):
        material = Materials.query.filter_by(material_name=material_name).first()
        if not material:
            return jsonify({"status": "fail", "message": "Material not found!"}, 404)

        db.session.delete(material)
        db.session.commit()
        return jsonify({"status": "success", "message": "Material deleted successfully!"}, 200)
