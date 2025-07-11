from .basemodel import BaseModel
from app.extensions import db
from sqlalchemy.orm import validates, relationship
from .place_amenity import place_amenity


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)

    owner = db.relationship("User", backref="places")
    amenities = relationship(
        "Amenity",
        secondary=place_amenity,
        back_populates="places",
        lazy="subquery"
    )

    @validates('title')
    def validate_title(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if not value.strip():
            raise ValueError("Title cannot be empty")
        if len(value) > 100:
            raise ValueError("Title must be less than or equal to 100 characters")
        return value

    @validates('price')
    def validate_price(self, key, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number")
        if value < 0:
            raise ValueError("Price must be positive.")
        return float(value)

    @validates('latitude')
    def validate_latitude(self, key, value):
        if not isinstance(value, float):
            raise TypeError("Latitude must be a float")
        if value < -90 or value > 90:
            raise ValueError("Latitude must be between -90 and 90")
        return value

    @validates('longitude')
    def validate_longitude(self, key, value):
        if not isinstance(value, float):
            raise TypeError("Longitude must be a float")
        if value < -180 or value > 180:
            raise ValueError("Longitude must be between -180 and 180")
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id
        }

    def to_dict_list(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner': self.owner.to_dict() if self.owner else None,
            'amenities': [],
            'reviews': []
        }
