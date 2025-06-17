from models import BaseModel


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
