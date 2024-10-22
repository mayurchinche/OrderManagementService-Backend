from flask import jsonify

from src.models.material_modules import MaterialModules
from src.db.db import db

class ModuleService:
    @staticmethod
    def add_module(material_name, module_name):
        try:
            new_module = MaterialModules(material_name=material_name, module_name=module_name)
            db.session.add(new_module)
            db.session.commit()
            return jsonify({"message": "Module added successfully"},200)
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)},500)

    @staticmethod
    def update_module(material_name, old_module_name, new_module_name):
        try:
            module = MaterialModules.query.filter_by(material_name=material_name, module_name=old_module_name).first()
            if not module:
                return jsonify({"error": "Module not found"},404)
            module.module_name = new_module_name
            db.session.commit()
            return jsonify({"message": "Module updated successfully"},201)
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)},500)

    @staticmethod
    def get_modules(material_name):
        try:
            modules = MaterialModules.query.filter_by(material_name=material_name).all()
            return jsonify({"modules": [module.to_dict() for module in modules]},200)
        except Exception as e:
            return jsonify({"error": str(e)},500)

    @staticmethod
    def delete_module(material_name, module_name):
        try:
            module = MaterialModules.query.filter_by(material_name=material_name, module_name=module_name).first()
            if not module:
                return jsonify({"error": "Module not found"},404)
            db.session.delete(module)
            db.session.commit()
            return jsonify({"message": "Module deleted successfully"},200)
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)},500)
