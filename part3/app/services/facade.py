from app.persistence.repository import SQLAlchemyRepository, InMemoryRepository, Repository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.extensions import db


class HBnBFacade:
    def __init__(self):
        self.user_repository = SQLAlchemyRepository(User)  # Switched to SQLAlchemyRepository
        self.place_repository = SQLAlchemyRepository(Place)
        self.review_repository = SQLAlchemyRepository(Review)
        self.amenity_repository = SQLAlchemyRepository(Amenity)

    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repository.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repository.get(user_id)

    def get_users(self):
        return self.user_repository.get_all()

    # Similarly, implement methods for other entities

    def get_user_by_email(self, email):
        return self.user_repository.get_by_attribute('email', email)
    
    def update_user(self, user_id, user_data):
        user = self.user_repository.get(user_id)
        if not user:
            raise ValueError("User not found")   
        
        # Si password présent, hasher
        if 'password' in user_data and user_data['password']:
            user.hash_password(user_data['password'])

        self.user_repository.save(user)

    # AMENITY
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repository.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repository.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repository.update(amenity_id, amenity_data)

    # PLACE
    def create_place(self, place_data):
        user = self.user_repository.get_by_attribute('id', place_data['owner_id'])
        if not user:
            raise KeyError('Invalid input data')
        del place_data['owner_id']
        place_data['owner'] = user
        amenities = place_data.pop('amenities', None)
        if amenities:
            for a in amenities:
                amenity = self.get_amenity(a['id'])
                if not amenity:
                    raise KeyError('Invalid input data')
        place = Place(**place_data)
        self.place_repository.add(place)
        if amenities:
            for amenity in amenities:
                place.add_amenity(amenity)
        return place

    def get_place(self, place_id):
        return self.place_repository.get(place_id)

    def get_all_places(self):
        return self.place_repository.get_all()

    def update_place(self, place_id, place_data):
        self.place_repository.update(place_id, place_data)

    # REVIEWS
    def create_review(self, review_data):
        user = self.user_repository.get(review_data['user_id'])
        if not user:
            raise KeyError('Invalid input data')
        del review_data['user_id']
        review_data['user'] = user

        place = self.place_repository.get(review_data['place_id'])
        if not place:
            raise KeyError('Invalid input data')
        del review_data['place_id']
        review_data['place'] = place

        review = Review(**review_data)
        self.review_repository.add(review)
        return review

        
    def get_review(self, review_id):
        return self.review_repository.get(review_id)

    def get_all_reviews(self):
        return self.review_repository.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repository.get(place_id)
        if not place:
            raise KeyError('Place not found')
        return place.reviews

    def update_review(self, review_id, review_data):
        review = self.review_repository.get(review_id)
        if not review:
            raise ValueError("Review not found")
        self.review_repository.update(review_id, review_data)


    def delete_review(self, review_id):
        review = self.review_repository.get(review_id)
        
        user = self.user_repository.get(review.user.id)
        place = self.place_repository.get(review.place.id)

        user.delete_review(review)
        place.delete_review(review)
        self.review_repository.delete(review_id)
