from flask_restx import Namespace, Resource, fields
<<<<<<< HEAD
from flask import request
=======
>>>>>>> origin
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
<<<<<<< HEAD
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
=======
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place'),
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating between 1 and 5')
>>>>>>> origin
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
<<<<<<< HEAD
        """Register a new user"""
        data = request.get_json()
        if not data:
            return {"error": "No input data provided"}, 400
        if 'rating' in data and (data['rating'] < 1 or data['rating'] > 5):
            return {"error": "Rating must be between 1 and 5"}, 400
        

        user = facade.get_user(data.get('user_id'))
        if not user:
            return {"error": f"User with ID {data.get('user_id')} not found"}, 400
        

        place = facade.get_place(data.get('place_id'))
        if not place:
            return {"error": f"Place with ID {data.get('place_id')} not found"}, 400

        try:
            review = facade.create_review(data)
        except Exception as e:
            return {"error": str(e)}, 400


        return review.to_dict(), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Récupère tous les utilisateurs"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200

@api.route('/<review_id>')
=======
        """Create a new review"""
        data = api.payload
        try:
            review = facade.create_review(data)
            return {
                "id": review.id,
                "user_id": review.user.id,
                "place_id": review.place.id,
                "text": review.text,
                "rating": review.rating
            }, 201
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        results = []
        for r in reviews:
            results.append({
                "id": r.id,
                "user_id": r.user.id,
                "place_id": r.place.id,
                "text": r.text,
                "rating": r.rating
            })
        return results, 200

@api.route('/<string:review_id>')
>>>>>>> origin
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
<<<<<<< HEAD
        """Get user details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200
=======
        """Get review by ID"""
        try:
            review = facade.get_review(review_id)
            return {
                "id": review.id,
                "user_id": review.user.id,
                "place_id": review.place.id,
                "text": review.text,
                "rating": review.rating
            }, 200
        except Exception as e:
            return {"error": str(e)}, 404
>>>>>>> origin

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
<<<<<<< HEAD
        """Update user details"""
        data = request.get_json()
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if 'rating' in data and (data['rating'] < 1 or data['rating'] > 5):
            return {"error": "Rating must be between 1 and 5"}, 400
        
        # Tu peux aussi vérifier si user_id et place_id existent si tu autorises leur modification
        if 'user_id' in data:
            user = facade.get_user(data['user_id'])
            if not user:
                return {"error": f"User with ID {data['user_id']} not found"}, 400
        if 'place_id' in data:
            place = facade.get_place(data['place_id'])
            if not place:
                return {"error": f"Place with ID {data['place_id']} not found"}, 400

        try:
            updated_review = facade.update_review(review_id, data)
        except Exception as e:
            return {"error": str(e)}, 400

        return {
            "message": "Review updated successfully",
            "review": updated_review.to_dict()
        }, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        try:
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except ValueError as e:
            return {"error": str(e)}, 404
        

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        reviews = facade.get_reviews_by_place(place_id)
        return [r.to_dict() for r in reviews], 200
=======
        """Update review"""
        data = api.payload
        try:
            review = facade.update_review(review_id, data)
            if not review:
                return {"error": "Review not found"}, 404
            return {
                "message": "Review updated successfully",
                "id": review.id,
                "user_id": review.user.id,
                "place_id": review.place.id,
                "text": review.text,
                "rating": review.rating
            }, 200
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete review"""
        try:
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 404
>>>>>>> origin
