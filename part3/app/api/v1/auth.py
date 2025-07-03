from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Authentiation operations')

# Validation des données envoyées par le client
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authentifie utilisateur et retourne un token JWT"""
        
        # Récupérer l'utilisateur en base
        credentials = api.payload
        user = facade.get_user_by_email(credentials['email'])

        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401
        
        # Creation du token JWT avec user id et le flag is_admin
        access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})

        return {'access_token': access_token}, 200