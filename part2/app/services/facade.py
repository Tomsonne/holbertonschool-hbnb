from app.models.place import Place
from app.models.user import User
from app.models.base_model import BaseModel
from app.models.amenity import Amenity
from app.models.review import Review
from app.persistence.repository import InMemoryRepository

import uuid
import re


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

#USER

    def create_user(self, user_data):
        email = user_data.get('email')
        if email is None or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            return None
        self.user_repo.update(user_id, user_data)
        return user
    
    def get_all_users(self):
        return self.user_repo.get_all()
# PLACE

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def create_place(self, place_data):
        owner_id = place_data.get("owner_id")
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError(f"Owner with ID {owner_id} not found")

        amenity_ids = place_data.get("amenities", [])
        amenities = []
        for aid in amenity_ids:
            amenity = self.get_amenity(aid)
            if not amenity:
                raise ValueError(f"Amenity with ID {aid} not found")
            amenities.append(amenity)

        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=owner
        )

        for amenity in amenities:
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place


    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)
    

     # AMENITY
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)
    
    def delete_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise Exception("Amenity not found")
        self.amenity_repo.delete(amenity_id)


    # REVIEW
    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        rating = review_data.get('rating')
        text = review_data.get('text', '')

        # Vérifier existence user et place
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("Invalid or missing user_id")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Invalid or missing place_id")

        # Vérification du rating
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        # Construire le Review avec objets User et Place
        review = Review(user=user, place=place, text=text, rating=rating)
        self.review_repo.add(review)
        return review


    def get_review(self, review_id):
        review =  self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        return review

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        if not place_id:
            raise ValueError("Missing place_id")
    
        all_reviews = self.review_repo.get_all()
        filtered_reviews = [review for review in all_reviews if review.place_id == place_id]
        return filtered_reviews


    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")

        self.review_repo.delete(review_id)