from app.models.place import Place
from app.models.user import User
from app.models.BaseModel import BaseModel
from app.models.amenitie import Amenity
from app.models.review import Review
from app.persistence.repository import InMemoryRepository

import uuid

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

#USER

    def create_user(self, user_data):
        user = User(**user_data)
        #try catch pour gerer email
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


#AMENITY

    def create_amenity(self, amenity_data):
        amenitie = Amenity(**amenity_data)
        #try catch pour gerer email
        self.amenity_repo.add(amenitie)
        return amenitie

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None  # ou lève une exception si tu préfères

        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity


# PLACE

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def create_place(self, place_data):
        # 1. Récupérer le User à partir de owner_id
        owner_id = place_data.get("owner_id")
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError(f"Owner with ID {owner_id} not found")

        # 2. Récupérer les objets Amenity à partir des IDs
        amenity_ids = place_data.get("amenities", [])
        amenities = []
        for aid in amenity_ids:
            amenity = self.get_amenity(aid)
            if not amenity:
                raise ValueError(f"Amenity with ID {aid} not found")
            amenities.append(amenity)

        # 3. Créer la Place SANS passer amenities
        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=owner
        )

        # 4. Ajouter les amenities à la main ensuite
        for amenity in amenities:
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place


    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)


#REVIEW 

    def create_review(self, data: dict) -> Review:
        # Valide que user et place existent
        user_id = data.get('user_id')
        place_id = data.get('place_id')
        user = self.user_repo.get(user_id)
        place = self.place_repo.get(place_id)

        if user is None:
            raise ValueError(f"User with ID {user_id} not found")
        if place is None:
            raise ValueError(f"Place with ID {place_id} not found")

        review = Review(
            text=data.get('text'),
            rating=data.get('rating'),
            user=user,
            place=place
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return list(self.review_repo.values())

    def update_review(self, review_id, review_data):
        self.place_repo.update(review_id, review_data)
        return self.place_repo.get(review_id)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if review is None:
            del self.review_repo[review_id]
        else:
            raise ValueError("Review not found")

    def get_reviews_by_place(self, place_id):
        if not self.get_place(place_id):
            raise ValueError("Place not found")
        return [
            r for r in self.review_repo.get_all()
            if r.place == place_id
        ]
