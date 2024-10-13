# src/controllers/material_controller.py
from flask import jsonify, request
from numpy.f2py.auxfuncs import throw_error

from src.services.material_service import MaterialService

class MaterialController:

    @staticmethod
    def get_all_materials():
        try:
            return MaterialService.get_all_materials()
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def add_material(data):
        try:
            material_name = data.get("material_name")
            description = data.get("description")
            return MaterialService.add_material(material_name,description)
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def delete_material(material_id):
        try:
            return MaterialService.delete_material(material_id)
        except Exception as e:
            return {"error": str(e)}, 500
