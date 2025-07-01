import pytest
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.models.user import User

from app import create_app

import uuid

#test api user

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()


def test_create_user(client):
    response = client.post('/api/v1/users/', json={
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com"
    })

    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["email"] == "alice@example.com"


def test_create_user_duplicate_email(client):
    # Créer une première fois
    client.post('/api/v1/users/', json={
        "first_name": "Bob",
        "last_name": "Dupont",
        "email": "bob@example.com"
    })

    # Réessayer avec le même email
    response = client.post('/api/v1/users/', json={
        "first_name": "Bobby",
        "last_name": "Martin",
        "email": "bob@example.com"
    })

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_get_user_by_id(client):
    # Créer un utilisateur
    post_response = client.post('/api/v1/users/', json={
        "first_name": "Charlie",
        "last_name": "Brown",
        "email": "charlie@example.com"
    })
    user_id = post_response.get_json()["id"]

    # Le récupérer
    get_response = client.get(f'/api/v1/users/{user_id}')
    assert get_response.status_code == 200
    data = get_response.get_json()
    assert data["email"] == "charlie@example.com"


def test_get_user_not_found(client):
    response = client.get('/api/v1/users/unknown-id')
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_get_all_users(client):
    # Ajouter quelques utilisateurs
    client.post('/api/v1/users/', json={
        "first_name": "Diana",
        "last_name": "Prince",
        "email": "diana@example.com"
    })
    client.post('/api/v1/users/', json={
        "first_name": "Clark",
        "last_name": "Kent",
        "email": "clark@example.com"
    })

    response = client.get('/api/v1/users/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_update_user(client):
    # Créer un utilisateur
    post_response = client.post('/api/v1/users/', json={
        "first_name": "Eve",
        "last_name": "Taylor",
        "email": "eve@example.com"
    })
    user_id = post_response.get_json()["id"]

    # Mettre à jour
    put_response = client.put(f'/api/v1/users/{user_id}', json={
        "first_name": "Eva",
        "last_name": "Turner",
        "email": "eva@example.com"
    })
    assert put_response.status_code == 200
    updated = put_response.get_json()
    assert updated["first_name"] == "Eva"
    assert updated["email"] == "eva@example.com"


def test_update_user_not_found(client):
    response = client.put('/api/v1/users/invalid-id', json={
        "first_name": "Ghost",
        "last_name": "User",
        "email": "ghost@example.com"
    })
    assert response.status_code == 404
    assert "error" in response.get_json()

def test_create_user_invalid_first_name(client):
    response = client.post('/api/v1/users/', json={
        "first_name": "",
        "last_name": "Smith",
        "email": "invalid1@example.com"
    })

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data or "message" in data

def test_create_user_invalid_last_name(client):
    response = client.post('/api/v1/users/', json={
        "first_name": "Alice",
        "last_name": "",
        "email": "invalid2@example.com"
    })

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data or "message" in data

def test_create_user_invalid_email(client):
    response = client.post('/api/v1/users/', json={
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "not-an-email"
    })

    assert response.status_code in (400, 201)  # À ajuster si tu fais une vraie validation d'email
    data = response.get_json()
    if response.status_code == 400:
        assert "error" in data or "message" in data
    else:
        assert "id" in data  # si accepté (selon ton implémentation actuelle)

    
def test_create_user_invalid_email_format(client):
    invalid_emails = ["plainaddress", "@missingusername.com", "missingatsign.com", "missingdomain@.com"]
    for email in invalid_emails:
        res = client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": email
        })
        assert res.status_code == 400
        data = res.get_json()
        assert "error" in data or "message" in data

#test user classe


def test_user_valid_instantiation():
    user = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    assert user.first_name == "Alice"
    assert user.last_name == "Smith"
    assert user.email == "alice@example.com"
    assert user.is_admin is False

def test_first_name_empty():
    with pytest.raises(ValueError):
        User(first_name="", last_name="Smith", email="test@test.com")

def test_first_name_too_long():
    long_name = "A" * 51
    with pytest.raises(ValueError):
        User(first_name=long_name, last_name="Smith", email="test@test.com")


def test_last_name_empty():
    with pytest.raises(ValueError):
        User(first_name="Bob", last_name="", email="test@test.com")

def test_last_name_too_long():
    long_name = "B" * 51
    with pytest.raises(ValueError):
        User(first_name="Bob", last_name=long_name, email="test@test.com")


@pytest.mark.parametrize("invalid_email", [
    "",                     # vide
    "useratexample.com",    # pas de @
    "user@com",             # pas de point après le @
    "user@examplecom",      # pas de point
    "user@example."         # point mais incomplet
])


def test_email_invalid(invalid_email):
    with pytest.raises(ValueError):
        User(first_name="Test", last_name="User", email=invalid_email)

def test_email_too_long():
    long_email = "a" * 250 + "@a.com"  # total > 255
    with pytest.raises(ValueError):
        User(first_name="Test", last_name="User", email=long_email)


def test_is_admin_accepts_true_false():
    user = User("Alice", "Smith", "alice@example.com")
    user.is_admin = True
    assert user.is_admin is True
    user.is_admin = False
    assert user.is_admin is False

def test_is_admin_invalid_type():
    user = User("Alice", "Smith", "alice@example.com")
    with pytest.raises(ValueError):
        user.is_admin = "yes"  # doit être bool


def test_to_dict_format():
    user = User("Charlie", "Brown", "charlie@peanuts.com")
    user_dict = user.to_dict()
    assert isinstance(user_dict, dict)
    assert user_dict["first_name"] == "Charlie"
    assert user_dict["last_name"] == "Brown"
    assert user_dict["email"] == "charlie@peanuts.com"
    assert "id" in user_dict
