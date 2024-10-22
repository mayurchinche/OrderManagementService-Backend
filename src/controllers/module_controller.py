from flask import jsonify
from src.services.module_service import ModuleService

class ModuleController:
    @staticmethod
    def add_module(data):
        material_name = data.get('material_name')
        module_name = data.get('module_name')
        return ModuleService.add_module(material_name, module_name)

    @staticmethod
    def update_module(material_name, module_name, data):
        new_module_name = data.get('module_name')
        return ModuleService.update_module(material_name, module_name, new_module_name)

    @staticmethod
    def get_modules(material_name):
        return ModuleService.get_modules(material_name)

    @staticmethod
    def delete_module(material_name, module_name):
        return ModuleService.get_modules(material_name)
