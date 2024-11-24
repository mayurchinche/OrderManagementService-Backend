from src.db.db import db

from src.db.db import db


class MaterialModules(db.Model):
    __tablename__ = 'material_modules'

    material_name = db.Column(db.String(100), db.ForeignKey('materials.material_name'), primary_key=True)
    module_name = db.Column(db.String(100), primary_key=True)

    # Correct backref to avoid conflicts
    material = db.relationship("Materials", backref="material_associations")
    # module = db.relationship("Modules", backref="module_associations")

    def __repr__(self):
        return f"<MaterialModules {self.material_name} - {self.module_name}>"

    def to_dict(self):
        return {
            "material_name": self.material_name,
            "module_name": self.module_name
        }
