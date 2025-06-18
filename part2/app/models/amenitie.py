#!/usr/bin/python3

from app.models.BaseModel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not value or len(value) > 50:
            raise ValueError("Prénom requis, 50 caractères max")
        self.__name = value

    def to_dict(self):
        return {
            'name': self.name,
            }
