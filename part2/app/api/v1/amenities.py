from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        data = api.payload
        if not data or not data.get("name") or data.get("name").strip() == "":
            return {'error': 'Name is required'}, 400

        try:
            new_amenity = facade.create_amenity(data)
            return {
                "message": "Amenity created successfully",
                "id": new_amenity.id,
                "name": new_amenity.name
            }, 201

        except Exception as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        results = [a.to_dict() for a in amenities]
        return results, 200

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        data = api.payload

        if not data or not data.get("name") or data.get("name").strip() == "":
            return {'error': 'Name is required'}, 400
        
        updated_amenity = facade.update_amenity(amenity_id, data)
        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404

        return {
            "message": "Amenity updated successfully",
            "id": updated_amenity.id,
            "name": updated_amenity.name
        }, 200
    
    @api.response(200, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """Delete an amenity"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        facade.delete_amenity(amenity_id)
        return {"message": "Amenity deleted successfully"}, 200
