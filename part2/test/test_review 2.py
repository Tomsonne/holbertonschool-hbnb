import pytest
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app import create_app
import uuid

from app.models.review import Review
from app.models.user import User
from app.models.place import Place

#test api review

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()

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

#test classe review

@pytest.fixture
def sample_user():
    return User(first_name="John", last_name="Doe", email="john@example.com")

@pytest.fixture
def sample_place(sample_user):
    return Place(
        title="Villa Test",
        description="Grande villa avec piscine",
        price=200,
        latitude=40.0,
        longitude=3.0,
        owner=sample_user
    )

@pytest.fixture
def sample_review(sample_place, sample_user):
    return Review(
        text="Super endroit !",
        rating=5,
        place=sample_place,
        user=sample_user
    )

def test_review_valid_instantiation(sample_review):
    assert sample_review.text == "Super endroit !"
    assert sample_review.rating == 5
    assert isinstance(sample_review.place, Place)
    assert isinstance(sample_review.user, User)

def test_review_text_empty(sample_place, sample_user):
    with pytest.raises(ValueError):
        Review(text="", rating=4, place=sample_place, user=sample_user)

def test_review_text_wrong_type(sample_place, sample_user):
    with pytest.raises(TypeError):
        Review(text=123, rating=4, place=sample_place, user=sample_user)

def test_review_rating_invalid_low(sample_place, sample_user):
    with pytest.raises(ValueError):
        Review(text="Correct", rating=0, place=sample_place, user=sample_user)

def test_review_rating_invalid_high(sample_place, sample_user):
    with pytest.raises(ValueError):
        Review(text="Correct", rating=6, place=sample_place, user=sample_user)

def test_review_rating_not_int(sample_place, sample_user):
    with pytest.raises(TypeError):
        Review(text="Correct", rating="5", place=sample_place, user=sample_user)

def test_review_place_invalid_type(sample_user):
    with pytest.raises(TypeError):
        Review(text="Bien", rating=4, place="not_a_place", user=sample_user)

def test_review_user_invalid_type(sample_place):
    with pytest.raises(TypeError):
        Review(text="Bien", rating=4, place=sample_place, user="not_a_user")

def test_review_to_dict(sample_review):
    data = sample_review.to_dict()
    assert data["text"] == sample_review.text
    assert data["rating"] == sample_review.rating
    assert data["place_id"] == sample_review.place.id
    assert data["user_id"] == sample_review.user.id
