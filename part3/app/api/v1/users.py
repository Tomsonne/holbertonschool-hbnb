from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# User creation model
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# User update model (excluding email and password)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})


@api.route('/')
class UserList(Resource):
    @api.doc(security='apikey')
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(409, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Register a new user (Admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        existing = facade.get_user_by_email(user_data['email'])
        if existing:
            return {'error': 'Email already registered'}, 409

        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400

    @api.doc(security='apikey')
    @jwt_required()
    @api.response(200, 'List of users retrieved successfully')
    @api.response(403, 'Admin privileges required')
    def get(self):
        """Retrieve list of users (Admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        users = facade.get_users()
        return [user.to_dict() for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Retrieve details of a specific user"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_update_model, validate=True)
    @api.doc(security='apikey')
    @jwt_required()
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update a user's info"""
        current_user_id = get_jwt_identity()

        # Check if user exists
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Only the user themself can update their data
        if current_user_id != user_id:
            return {'error': 'Forbidden'}, 403

        updates = api.payload or {}
        if 'email' in updates or 'password' in updates:
            return {'error': 'You cannot modify email or password'}, 400

        try:
            updated = facade.update_user(user_id, updates)
            return updated.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400
