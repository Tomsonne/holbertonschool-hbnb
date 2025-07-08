from app import create_app
from app.services import facade

app = create_app()
app.app_context().push()

admin_data = {
    'first_name': 'Admin',
    'last_name': 'User',
    'email': 'admin@example.com',
    'password': 'adminpass',
    'is_admin': True
}

# Supprimer s’il existe déjà
existing = facade.get_user_by_email(admin_data['email'])
if existing:
    print(existing)
    print("Admin déjà existant.")
else:
    new_admin = facade.create_user(admin_data)
    print("Admin créé avec succès :", new_admin.to_dict())
