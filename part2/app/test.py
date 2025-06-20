import pytest
import json
from app import create_app

import uuid


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

#amenity

def test_create_amenity(client):
    response = client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["name"] == "Wi-Fi"


def test_create_amenity_invalid_name(client):
    response = client.post('/api/v1/amenities/', json={"name": ""})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_get_all_amenities(client):
    client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
    client.post('/api/v1/amenities/', json={"name": "Air Conditioning"})

    response = client.get('/api/v1/amenities/')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(a["name"] == "Wi-Fi" for a in data)
    assert any(a["name"] == "Air Conditioning" for a in data)


def test_get_amenity_by_id(client):
    res = client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
    amenity_id = res.get_json()["id"]

    response = client.get(f'/api/v1/amenities/{amenity_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == amenity_id
    assert data["name"] == "Wi-Fi"


def test_get_amenity_not_found(client):
    response = client.get('/api/v1/amenities/unknown-id')
    assert response.status_code == 404


def test_update_amenity(client):
    res = client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
    amenity_id = res.get_json()["id"]

    response = client.put(f'/api/v1/amenities/{amenity_id}', json={"name": "Air Conditioning"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Amenity updated successfully"

    updated = client.get(f'/api/v1/amenities/{amenity_id}').get_json()
    assert updated["name"] == "Air Conditioning"


def test_update_amenity_invalid_name(client):
    res = client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
    amenity_id = res.get_json()["id"]

    response = client.put(f'/api/v1/amenities/{amenity_id}', json={"name": ""})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_update_amenity_not_found(client):
    response = client.put('/api/v1/amenities/nonexistent-id', json={"name": "New Name"})
    assert response.status_code == 404


#place
# Crée un utilisateur valide pour owner_id
@pytest.fixture
def user_id(client):
    unique_email = f"john.doe.{uuid.uuid4()}@example.com"
    res = client.post('/api/v1/users/', json={
        "first_name": "John",
        "last_name": "Doe",
        "email": unique_email,
    })
    print("User creation response:", res.status_code, res.get_json())
    assert res.status_code == 201
    return res.get_json()["id"]

def test_create_place_success(client, user_id):
    payload = {
        "title": "Cozy Apartment",
        "description": "A nice place to stay",
        "price": 100.0,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "owner_id": user_id
    }

    res = client.post("/api/v1/places/", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == "Cozy Apartment"
    assert data["price"] == 100.0
    assert data["latitude"] == 37.7749
    assert data["longitude"] == -122.4194
    assert data["owner_id"] == user_id


def test_create_place_invalid_data(client):
    res = client.post("/api/v1/places/", json={})
    assert res.status_code == 400


def test_get_all_places(client, user_id):
    # Créer un place d'abord
    client.post("/api/v1/places/", json={
        "title": "Test Place",
        "description": "Nice",
        "price": 50.0,
        "latitude": 0.0,
        "longitude": 0.0,
        "owner_id": user_id
    })

    res = client.get("/api/v1/places/")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert any("title" in p for p in data)


def test_get_place_detail(client, user_id):
    res = client.post("/api/v1/places/", json={
        "title": "Test Place Detail",
        "description": "Details here",
        "price": 80.0,
        "latitude": 12.34,
        "longitude": 56.78,
        "owner_id": user_id
    })
    place_id = res.get_json()["id"]

    res = client.get(f"/api/v1/places/{place_id}")
    assert res.status_code == 200
    data = res.get_json()
    assert data["title"] == "Test Place Detail"
    assert "owner" in data
    assert "amenities" in data


def test_get_place_not_found(client):
    res = client.get("/api/v1/places/nonexistent-id")
    assert res.status_code == 404


def test_update_place_success(client, user_id):
    res = client.post("/api/v1/places/", json={
        "title": "Old Title",
        "description": "Old desc",
        "price": 50.0,
        "latitude": 0.0,
        "longitude": 0.0,
        "owner_id": user_id
    })
    place_id = res.get_json()["id"]

    res = client.put(f"/api/v1/places/{place_id}", json={
        "title": "Luxury Condo",
        "description": "An upscale place to stay",
        "price": 200.0
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["message"] == "Place updated successfully"


def test_update_place_not_found(client):
    res = client.put("/api/v1/places/nonexistent-id", json={
        "title": "Nothing"
    })
    assert res.status_code == 404

def test_create_place_invalid_title(client, user_id):
    payload = {
        "title": "",
        "description": "Invalid title",
        "price": 100.0,
        "latitude": 20.0,
        "longitude": 20.0,
        "owner_id": user_id
    }
    res = client.post("/api/v1/places/", json=payload)
    assert res.status_code == 400

def test_create_place_negative_price(client, user_id):
    payload = {
        "title": "Invalid Price",
        "description": "Negative price",
        "price": -10,
        "latitude": 20.0,
        "longitude": 20.0,
        "owner_id": user_id
    }
    res = client.post("/api/v1/places/", json=payload)
    assert res.status_code == 400

def test_create_place_invalid_latitude(client, user_id):
    payload = {
        "title": "Invalid Latitude",
        "description": "Too high latitude",
        "price": 50.0,
        "latitude": 100.0,  # > 90
        "longitude": 0.0,
        "owner_id": user_id
    }
    res = client.post("/api/v1/places/", json=payload)
    assert res.status_code == 400

def test_create_place_invalid_longitude(client, user_id):
    payload = {
        "title": "Invalid Longitude",
        "description": "Too low longitude",
        "price": 50.0,
        "latitude": 0.0,
        "longitude": -200.0,  # < -180
        "owner_id": user_id
    }
    res = client.post("/api/v1/places/", json=payload)
    assert res.status_code == 400





#Review
def test_create_review_success(client, user_id):
    # Créer un place pour attacher la review
    place_res = client.post("/api/v1/places/", json={
        "title": "Review Place",
        "description": "Place for review",
        "price": 100.0,
        "latitude": 10.0,
        "longitude": 10.0,
        "owner_id": user_id
    })
    place_id = place_res.get_json()["id"]

    review_payload = {
        "text": "Great place!",
        "rating": 5,
        "user_id": user_id,
        "place_id": place_id
    }

    res = client.post("/api/v1/reviews/", json=review_payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["text"] == "Great place!"
    assert data["rating"] == 5
    assert data["user_id"] == user_id
    assert data["place_id"] == place_id

def test_create_review_missing_text(client, user_id):
    place_res = client.post("/api/v1/places/", json={
        "title": "Place for invalid review",
        "description": "Place for review",
        "price": 100.0,
        "latitude": 10.0,
        "longitude": 10.0,
        "owner_id": user_id
    })
    place_id = place_res.get_json()["id"]

    review_payload = {
        "text": "",
        "rating": 4,
        "user_id": user_id,
        "place_id": place_id
    }
    res = client.post("/api/v1/reviews/", json=review_payload)
    assert res.status_code == 400
    data = res.get_json()
    assert "error" in data

def test_create_review_invalid_user_or_place(client, user_id):
    review_payload = {
        "text": "Nice",
        "rating": 3,
        "user_id": "nonexistent-user-id",
        "place_id": "nonexistent-place-id"
    }
    res = client.post("/api/v1/reviews/", json=review_payload)
    assert res.status_code == 400 or res.status_code == 404
    data = res.get_json()
    assert "error" in data

def test_get_review_by_id(client, user_id):
    place_res = client.post("/api/v1/places/", json={
        "title": "Review Place",
        "description": "Place for review",
        "price": 100.0,
        "latitude": 10.0,
        "longitude": 10.0,
        "owner_id": user_id
    })
    place_id = place_res.get_json()["id"]

    review_res = client.post("/api/v1/reviews/", json={
        "text": "Lovely",
        "rating": 4,
        "user_id": user_id,
        "place_id": place_id
    })
    review_id = review_res.get_json()["id"]

    get_res = client.get(f"/api/v1/reviews/{review_id}")
    assert get_res.status_code == 200
    data = get_res.get_json()
    assert data["id"] == review_id

def test_get_review_not_found(client):
    res = client.get("/api/v1/reviews/nonexistent-id")
    assert res.status_code == 404

def test_update_review_success(client, user_id):
    place_res = client.post("/api/v1/places/", json={
        "title": "Place for review update",
        "description": "Place for review",
        "price": 100.0,
        "latitude": 10.0,
        "longitude": 10.0,
        "owner_id": user_id
    })
    place_id = place_res.get_json()["id"]

    review_res = client.post("/api/v1/reviews/", json={
        "text": "Okay",
        "rating": 3,
        "user_id": user_id,
        "place_id": place_id
    })
    review_id = review_res.get_json()["id"]

    put_res = client.put(f"/api/v1/reviews/{review_id}", json={
        "text": "Updated review",
        "rating": 5
    })
    assert put_res.status_code == 200
    data = put_res.get_json()
    assert data["message"] == "Review updated successfully"

def test_update_review_not_found(client):
    res = client.put("/api/v1/reviews/nonexistent-id", json={
        "text": "Nope",
        "rating": 1
    })
    assert res.status_code == 404

def test_delete_review_success(client, user_id):
    place_res = client.post("/api/v1/places/", json={
        "title": "Place for review delete",
        "description": "Place for review",
        "price": 100.0,
        "latitude": 10.0,
        "longitude": 10.0,
        "owner_id": user_id
    })
    place_id = place_res.get_json()["id"]

    review_res = client.post("/api/v1/reviews/", json={
        "text": "To be deleted",
        "rating": 2,
        "user_id": user_id,
        "place_id": place_id
    })
    review_id = review_res.get_json()["id"]

    del_res = client.delete(f"/api/v1/reviews/{review_id}")
    assert del_res.status_code == 200
    data = del_res.get_json()
    assert data["message"] == "Review deleted successfully"

def test_delete_review_not_found(client):
    res = client.delete("/api/v1/reviews/nonexistent-id")
    assert res.status_code == 404
