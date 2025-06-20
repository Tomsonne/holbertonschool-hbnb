from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place'),
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating between 1 and 5')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
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
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
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

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
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
