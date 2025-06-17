from models import BaseModel


class review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        self.__text = text
        self.__rating = rating
        self.__place = place
        self.__user = user


    def create_amenity(self, amenity_data):
        # Placeholder for logic to create an amenity
        pass

    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        pass

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        pass

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        pass