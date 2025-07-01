import pytest
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app import create_app
import uuid
from datetime import datetime
from app.models.amenity import Amenity
import time

#test api amenity

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()


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

#test amenity class

def test_amenity_instantiation():
    """Test de base : instanciation correcte"""
    ame = Amenity(name="Wi-Fi")
    assert ame.name == "Wi-Fi"
    assert isinstance(ame.id, str)
    assert ame.is_valid_uuid()
    assert isinstance(ame.created_at, datetime)
    assert isinstance(ame.updated_at, datetime)



def test_amenity_ignore_invalid_kwargs():
    """Les champs non autorisés ne sont pas ajoutés"""
    ame = Amenity(name="Spa", invalid_field="test")
    assert not hasattr(ame, "invalid_field")


def test_to_dict_returns_expected_structure():
    """Test du format retourné par to_dict"""
    ame = Amenity(name="Hammam")
    result = ame.to_dict()
    assert isinstance(result, dict)
    assert result["id"] == ame.id
    assert result["name"] == "Hammam"
    assert result["created_at"] == ame.created_at.isoformat()
    assert result["updated_at"] == ame.updated_at.isoformat()


def test_updated_at_changes_on_save():
    ame = Amenity(name="Parking")
    old_updated = ame.updated_at
    time.sleep(0.001)
    ame.save()
    assert ame.updated_at > old_updated
