from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields, reqparse
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})


# Define the model for updating user information (excluding email and password)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(409, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing = facade.get_user_by_email(user_data['email'])
        if existing:
            return {'error': 'Email already registered'}, 409

        try:
            new_user = facade.create_user(user_data)
            return new_user.to_dict(), 201
        except Exception as e:
            return {'error': str(e)}, 400
        
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of users"""
        users = facade.get_users()
        return [user.to_dict() for user in users], 200
    
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

       
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @api.response(403, 'Forbidden')
    @api.response(404, 'User not found')
    @api.doc(security='apikey')
    @jwt_required()
    def put(self, user_id):
        """Update a user's info (excluding email/password)"""
        current_user = get_jwt_identity()

        # 4a) Vérifier que le user existe
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # 4b) Seul soi-même peut modifier son profil
        if current_user != user_id:
            return {'error': 'Forbidden'}, 403

        # 4c) Empêcher modification de email/password
        updates = api.payload or {}
        if 'email' in updates or 'password' in updates:
            return {'error': 'You cannot modify email or password'}, 400

        try:
            updated = facade.update_user(user_id, updates)
            return updated.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 400