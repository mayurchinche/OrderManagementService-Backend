from src.db.db import db


class Materials(db.Model):
    __tablename__ = "materials"
    material_name = db.Column(db.String(255), primary_key=True,nullable=False, unique=True)
    description = db.Column(db.String(500))


    def __repr__(self):
        return f"<Materials {self.material_name}: {self.description}>"