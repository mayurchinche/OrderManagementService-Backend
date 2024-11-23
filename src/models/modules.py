from src.db.db import db

class Modules(db.Model):
    __tablename__ = "modules"
    module_name = db.Column(db.String(100), unique=True,  primary_key=True,nullable=False)

    def __init__(self, module_name):
        self.module_name = module_name
    def __repr__(self):
        return f"<Module {self.module_name}>"
