from app import db
from .basemodel import BaseModel
from sqlalchemy.orm import validates, relationship
from app.models.place_amenity import place_amenity


class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(50), nullable=False, unique=True)

    places = relationship(
        "Place",
        secondary=place_amenity,
        back_populates="amenities",
        lazy="subquery"
    )

    @validates("name")
    def _validate_name(self, key, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not value.strip():
            raise ValueError("Name cannot be empty")
        if len(value) > 50:
            raise ValueError("Name must be 50 characters max.")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
