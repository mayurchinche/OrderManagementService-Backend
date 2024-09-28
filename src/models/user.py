# src/model/user.py
from flask_sqlalchemy import SQLAlchemy

from src.db.db import  db

class User(db.Model):
    __tablename__ = 'users'

    user_name = db.Column(db.String(80), unique=True, nullable=False)  # Changed to user_name
    user_password = db.Column(db.String(128), unique=True,primary_key=True,nullable=False)  # Added user_password
    contact_number = db.Column(db.String(15), nullable=False)  # Added contact_number

    def __repr__(self):
        return f'<User {self.user_name}>'

