from src.models.material_modules import MaterialModules
from src.db.db import db

class ModuleService:
    @staticmethod
    def add_module(material_name, module_name):
        try:
            new_module = MaterialModules(material_name=material_name, module_name=module_name)
            db.session.add(new_module)
            db.session.commit()
            return {"message": "Module added successfully"}
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}

    @staticmethod
    def update_module(material_name, old_module_name, new_module_name):
        try:
            module = MaterialModules.query.filter_by(material_name=material_name, module_name=old_module_name).first()
            if not module:
                return {"error": "Module not found"}
            module.module_name = new_module_name
            db.session.commit()
            return {"message": "Module updated successfully"}
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}

    @staticmethod
    def get_modules(material_name):
        try:
            modules = MaterialModules.query.filter_by(material_name=material_name).all()
            return {"modules": [module.to_dict() for module in modules]}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def delete_module(material_name, module_name):
        try:
            module = MaterialModules.query.filter_by(material_name=material_name, module_name=module_name).first()
            if not module:
                return {"error": "Module not found"}
            db.session.delete(module)
            db.session.commit()
            return {"message": "Module deleted successfully"}
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}
