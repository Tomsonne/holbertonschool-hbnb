#!/usr/bin/python3
from app.models.base_model import BaseModel
from app.models.user import User



class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []   # Liste des reviews associées
        self.amenities = [] # Liste des équipements associés

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if not value or len(value) > 100:
            raise ValueError("Le titre est requis (max 100 caractères)")
        self.__title = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        if not value or len(value) > 500:
            raise ValueError("La description est requise (max 500 caractères)")
        self.__description = value

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if not (isinstance(value, int) or isinstance(value, float)) or value < 0:
            raise ValueError("Le prix doit être un nombre positif")
        self.__price = value

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        if not (isinstance(value, float) or isinstance(value, int)) or not (-90 <= value <= 90):
            raise ValueError("La latitude doit être un nombre entre -90 et 90")
        self.__latitude = float(value)

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        if not (isinstance(value, float) or isinstance(value, int)) or not (-180 <= value <= 180):
            raise ValueError("La longitude doit être un nombre entre -180 et 180")
        self.__longitude = float(value)

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, value):
        if isinstance(value, User):
            self.__owner = value  # stocke son id
        elif isinstance(value, str) and value:
            self.__owner = value
        else:
            raise ValueError("Le propriétaire doit être une chaîne non vide ou un objet User")
        
    def add_review(self, review):
        """Ajouter une review à la liste."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Ajouter un équipement à la liste."""
        self.amenities.append(amenity)

    def to_dict(self, full=False):
        base = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id if hasattr(self.owner, 'id') else self.owner,
        }
        if full:
            base['owner'] = {
                'id': self.owner.id,
                'first_name': self.owner.first_name,
                'last_name': self.owner.last_name,
                'email': self.owner.email,
            }
            # Ajoute cette ligne pour inclure les amenities
            base['amenities'] = [amenity.to_dict() for amenity in self.amenities]
        return base
