from app import create_app, db
from app.models.user import User

def test_user_creation():
    app = create_app('config.DevelopmentConfig')
    print("→ URI:", app.config["SQLALCHEMY_DATABASE_URI"])

    with app.app_context():
        db.drop_all()
        db.create_all()

        user = User(
            first_name="Alice",
            last_name="Smith",
            email="alice@example.com",
            password="securepwd"
        )
        user.hash_password(user.password)
        db.session.add(user)
        db.session.commit()

        retrieved_user = User.query.filter_by(email="alice@example.com").first()

        assert retrieved_user is not None, "❌ Utilisateur non trouvé"
        assert retrieved_user.first_name == "Alice", "❌ Prénom incorrect"
        assert retrieved_user.verify_password("securepwd"), "❌ Mot de passe incorrect"

        print("✅ Test réussi :", retrieved_user.to_dict())

if __name__ == "__main__":
    test_user_creation()
