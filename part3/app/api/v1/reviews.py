from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')


review_model = api.model('ReviewInput', {
    'place_id': fields.String(required=True, description='ID of the place'),
    'text':     fields.String(required=True, description='Text of the review'),
    'rating':   fields.Integer(required=True, description='Rating of the place (1-5)')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data or business rule')
    @api.response(401, 'Unauthorized')
    @api.doc(security='apikey')
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        data = api.payload.copy()

        # Charger la place avant toute vérif
        place_id = data.get('place_id')
        if not place_id:
            return {'error': 'place_id is required'}, 400

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Pas de review sur sa propre place
        if place.owner.id == current_user:
            return {'error': 'You cannot review your own place'}, 400

        # Une seule review par place
        if any(r.user_id == current_user for r in place.reviews):
            return {'error': 'You have already reviewed this place'}, 400

        # création
        try:
            data['user_id'] = current_user
            new_review = facade.create_review(data)
            return new_review.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        return [r.to_dict() for r in facade.get_all_reviews()], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Review not found')
    @api.doc(security='apikey')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if review.user_id != current_user:
            return {'error': 'Forbidden'}, 403

        try:
            updated = facade.update_review(review_id, api.payload)
            return updated.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Review not found')
    @api.doc(security='apikey')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if review.user_id != current_user:
            return {'error': 'Forbidden'}, 403

        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400
