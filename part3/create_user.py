from app import create_app
from app.services import facade

app = create_app()
app.app_context().push()

user_data = {
    'first_name': 'beydi',
    'last_name': 'coulibaly',
    'email': 'beydi@example.com',
    'password': 'beydicoulibaly',
}

# Supprimer s’il existe déjà
existing = facade.get_user_by_email(user_data['email'])
if existing:
    print(existing)
    print("User déjà existant.")
else:
    new_user = facade.create_user(user_data)
    print("User créé avec succès :", new_user.to_dict())
