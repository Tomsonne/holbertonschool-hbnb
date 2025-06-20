import pytest
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app import create_app
import uuid

from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity


#test api place

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


#test classe place



@pytest.fixture
def sample_user():
    return User(first_name="Alice", last_name="Smith", email="alice@test.com")


@pytest.fixture
def sample_place(sample_user):
    return Place(
        title="Maison au bord du lac",
        description="Une belle maison avec vue sur le lac",
        price=120,
        latitude=48.85,
        longitude=2.35,
        owner=sample_user
    )


def test_place_valid_instantiation(sample_place):
    assert sample_place.title == "Maison au bord du lac"
    assert sample_place.price == 120
    assert isinstance(sample_place.owner, User)
    assert sample_place.latitude == 48.85
    assert sample_place.longitude == 2.35
    assert sample_place.reviews == []
    assert sample_place.amenities == []


def test_invalid_title():
    with pytest.raises(ValueError):
        Place(title="", description="ok", price=50, latitude=0, longitude=0, owner="user")


def test_invalid_description():
    with pytest.raises(ValueError):
        Place(title="ok", description="", price=50, latitude=0, longitude=0, owner="user")


def test_invalid_price():
    with pytest.raises(ValueError):
        Place(title="ok", description="ok", price=-5, latitude=0, longitude=0, owner="user")


def test_invalid_latitude():
    with pytest.raises(ValueError):
        Place(title="ok", description="ok", price=10, latitude=95, longitude=0, owner="user")


def test_invalid_longitude():
    with pytest.raises(ValueError):
        Place(title="ok", description="ok", price=10, latitude=0, longitude=190, owner="user")


def test_invalid_owner_type():
    with pytest.raises(ValueError):
        Place(title="ok", description="ok", price=10, latitude=0, longitude=0, owner=None)


def test_add_review(sample_place):
    sample_place.add_review("Très bien !")
    assert "Très bien !" in sample_place.reviews


def test_add_amenity(sample_place):
    a = Amenity(name="Wi-Fi")
    sample_place.add_amenity(a)
    assert a in sample_place.amenities


def test_to_dict_basic(sample_place):
    data = sample_place.to_dict()
    assert data["title"] == sample_place.title
    assert "owner_id" in data
    assert "owner" not in data
    assert "amenities" not in data


def test_to_dict_full(sample_place):
    sample_place.add_amenity(Amenity(name="Piscine"))
    data = sample_place.to_dict(full=True)
    assert "owner" in data
    assert "amenities" in data
    assert isinstance(data["amenities"], list)
    assert "first_name" in data["owner"]
