from src.db.db import db


class Materials(db.Model):
    __tablename__ = "materials"

    material_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    material_name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.String(500))

    def __repr__(self):
        return f"<Materials {self.material_id}: {self.material_name}>"