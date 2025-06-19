from app.models.base_model import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.__title = title
        self.__description = description
        self.__price = price
        self.__latitude = latitude
        self.__longitude = longitude
        self.__owner = owner
        self.__reviews = []  # List to store related reviews
        self.__amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        self.__reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.__amenities.append(amenity)
    

    @property
    def reviews(self):
        return self._reviews

    @property
    def amenities(self):
        return self._amenities


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner': self.owner,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'reviews': [review.to_dict() for review in self.reviews],
            'amenities': [amenity.to_dict() for amenity in self.amenities]
        }
