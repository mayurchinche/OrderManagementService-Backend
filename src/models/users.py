from email.policy import default

from flask_sqlalchemy import SQLAlchemy
# src/model/users.py

from src.db.db import  db

class User(db.Model):
    __tablename__ = 'users'

    user_name = db.Column(db.String(80), nullable=False)  # Changed to user_name
    user_password = db.Column(db.String(255), nullable=False)  # Added user_password
    contact_number = db.Column(db.String(20), unique=True,primary_key=True,nullable=False,index=True)  # Added contact_number
    role = db.Column(db.String(50), nullable=False,default='employee')  # Added role

    def __init__(self, user_name, user_password, contact_number, role):
        self.user_name = user_name
        self.user_password = user_password
        self.contact_number = contact_number
        self.role = role
    def __repr__(self):
        return f'<User {self.user_name}>'