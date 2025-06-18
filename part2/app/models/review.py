#!/usr/bin/python3
from app.models.BaseModel import BaseModel
from app.models.place import Place
from app.models.user import User


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        if not value or len(value) > 500:
            raise ValueError("Le texte de la review est requis (max 500 caractères)")
        self.__text = value

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("Le rating doit être un entier entre 1 et 5")
        self.__rating = value

    @property
    def place(self):
        return self.__place

    @place.setter
    def place(self, value):
        if isinstance(value, Place):
            self.__place = value.id  # on enregistre l'id de l'objet Place
        elif isinstance(value, str) and value.strip():
            self.__place = value
        else:
            raise ValueError("Le place_id est requis et doit être une chaîne ou un objet Place")


 


    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        if isinstance(value, User):
            self.__user = value.id
        elif isinstance(value, str) and value.strip():
            self.__user = value
        else:
            raise ValueError("L'utilisateur est requis et doit être une chaîne ou un objet User")
        
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place': self.place,
            'user': self.user
        }
