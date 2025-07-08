from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('places', description='Place operations')

# Modèle pour un amenity ID
amenity_id_model = api.model('AmenityID', {
    'id': fields.String(required=True, description='Amenity ID')
})

# Modèle d’entrée pour créer/modifier un Place
place_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, description="List of amenities IDs")
})

# Modèle utilisateur imbriqué (pour la réponse)
user_model = api.model('PlaceOwner', {
    'id': fields.String(description='Owner ID'),
    'first_name': fields.String(description='Owner first name'),
    'last_name': fields.String(description='Owner last name'),
    'email': fields.String(description='Owner email')
})

# Modèle de sortie pour un Place (hérite de PlaceInput + id + owner)
place_output_model = api.inherit('PlaceOutput', place_model, {
    'id': fields.String(description='Place ID'),
    'owner': fields.Nested(user_model, description='Owner details')
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.marshal_with(place_output_model, code=201)
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @api.doc(security='apikey')
    @jwt_required()
    def post(self):
        """Create a new place (with the auth)"""
        owner_id = get_jwt_identity()
        data = api.payload or {}
        data['owner_id'] = owner_id

        print("\n=== PAYLOAD REÇU DANS POST /places ===")
        print(data)
        print("=== FIN PAYLOAD ===\n")

        
        new_place = facade.create_place(data)
        return new_place.to_dict(), 201

    @api.marshal_with(place_output_model, as_list=True)
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.marshal_with(place_output_model)
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')
        return place.to_dict(), 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Place not found')
    @api.doc(security='apikey')
    @jwt_required()
    def put(self, place_id):
        """Update a place's info"""
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')
        if place.owner.id != current_user and not is_admin:
            api.abort(403, 'Forbidden')

        updated = facade.update_place(place_id, api.payload or {})
        return updated.to_dict(), 200

    @api.response(200, 'Place deleted successfully')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Place not found')
    @api.doc(security='apikey')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')
        if place.owner.id != current_user and not is_admin:
            api.abort(403, 'Forbidden')

        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200


@api.route('/<place_id>/amenities')
class PlaceAmenities(Resource):
    @api.expect(amenity_id_model, validate=True)
    @api.response(200, 'Amenity added successfully')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'Place not found')
    @api.doc(security='apikey')
    @jwt_required()
    def post(self, place_id):
        """Add an amenity to a place"""
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')
        if place.owner.id != current_user and not is_admin:
            api.abort(403, 'Forbidden')

        amenity_id = api.payload.get('id')
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(400, 'Invalid amenity ID')

        facade.add_amenity_to_place(place_id, amenity_id)
        return {'message': 'Amenity added successfully'}, 200


@api.route('/<place_id>/reviews/')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')
        return [review.to_dict() for review in place.reviews], 200
