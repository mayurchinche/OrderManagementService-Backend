from flask import jsonify
from src.services.module_service import ModuleService

class ModuleController:
    @staticmethod
    def add_module(data):
        material_name = data.get('material_name')
        module_name = data.get('module_name')
        response = ModuleService.add_module(material_name, module_name)
        return jsonify(response)

    @staticmethod
    def update_module(material_name, module_name, data):
        new_module_name = data.get('module_name')
        response = ModuleService.update_module(material_name, module_name, new_module_name)
        return jsonify(response)

    @staticmethod
    def get_modules(material_name):
        response = ModuleService.get_modules(material_name)
        return jsonify(response)

    @staticmethod
    def delete_module(material_name, module_name):
        response = ModuleService.delete_module(material_name, module_name)
        return jsonify(response)
