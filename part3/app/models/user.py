import re
from app.extensions import db, bcrypt
from .basemodel import BaseModel



class User(BaseModel):
    __tablename__ = 'users'

    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column("password", db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        if not isinstance(email, str) or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        self.email = email
        self.password = password
        self.is_admin = is_admin
        
        
    def set_password(self, plaintext_password):
         self._password = bcrypt.generate_password_hash(plaintext_password).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self._password, password)

    @property
    def password(self):
        raise AttributeError("password is write-only")

    @password.setter
    def password(self, plaintext_password):
        self.set_password(plaintext_password)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
        }