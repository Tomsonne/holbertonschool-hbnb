#!/usr/bin/python3
from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = False

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("Le prénom est requis et doit faire 50 caractères max")
        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("Le nom est requis et doit faire 50 caractères max")
        self.__last_name = value

    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, value):
        if (
            not value
            or len(value) > 255
            or value.count('@') != 1
            or '.' not in value.split('@')[1]
        ):
            raise ValueError("email invalide")

        self.__email = value


    @property
    def is_admin(self):
        return self.__is_admin
    
    @is_admin.setter
    def is_admin(self, value):
        if not isinstance(value, bool):
            raise ValueError("Saisir un booléen")
        self.__is_admin = value

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }

