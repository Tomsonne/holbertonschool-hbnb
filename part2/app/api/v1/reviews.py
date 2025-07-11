from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new review"""
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
        """Get all reviews"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200


@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update review"""
        data = request.get_json()
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if 'rating' in data and (data['rating'] < 1 or data['rating'] > 5):
            return {"error": "Rating must be between 1 and 5"}, 400

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
        """Delete review"""
        try:
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 404


@api.route('/places/<string:place_id>/reviews')
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
