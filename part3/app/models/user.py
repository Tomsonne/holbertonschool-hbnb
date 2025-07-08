from .basemodel import BaseModel
from app import db
import re
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    

    @validates('first_name', 'last_name')
    def validate_name(self, key, value):
        if not isinstance(value, str):
            raise TypeError(f"{key.replace('_', ' ').capitalize()} must be a string")
        if len(value) > 50:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be less than or equal to 50 characters")
        if not value.isalpha():
            raise ValueError(f"{key.replace('_', ' ').capitalize()} must be empty")
        return value

    @validates('email')
    def validate_email(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")
        return value

    @validates('is_admin')
    def validate_is_admin(self, key, value):
        if not isinstance(value, bool):
            raise TypeError("is_admin must be a boolean")
        return value

    def hash_password(self, password):
        """Hash le mot de passe en clair avant de le stocker."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Vérifie si un mot de passe correspond au hash stocké."""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }
