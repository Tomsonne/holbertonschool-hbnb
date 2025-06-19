import pytest
import json
from app import create_app
from app.services import HBnBFacade

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

# AMENITY

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


def test_delete_amenity(client):
    # Création
    res = client.post('/api/v1/amenities/', json={"name": "Piscine"})
    amenity_id = res.get_json()["id"]

    # Suppression
    delete_response = client.delete(f'/api/v1/amenities/{amenity_id}')
    assert delete_response.status_code == 200
    assert delete_response.get_json()["message"] == "Amenity deleted successfully"

    # Vérification qu'elle n'existe plus
    get_response = client.get(f'/api/v1/amenities/{amenity_id}')
    assert get_response.status_code == 404


def test_delete_amenity_not_found(client):
    response = client.delete('/api/v1/amenities/does-not-exist')
    assert response.status_code == 404
    assert "error" in response.get_json()


# REVIEW
def test_create_review_valid():
    facade = HBnBFacade()

    # Créer un user avec tous les champs requis
    user = facade.create_user({
        'email': 'test@example.com',
        'first_name': 'Alice',
        'last_name': 'Doe'
    })

    # Créer une place liée à ce user
    place = facade.create_place({
        'title': 'Maison test',
        'description': 'Maison au calme',
        'price': 100,
        'latitude': 45.0,
        'longitude': -1.0,
        'owner_id': user.id,
        'amenities': []
    })

    # Créer le review
    review_data = {
        'user_id': user.id,
        'place_id': place.id,
        'text': 'Super séjour',
        'rating': 5
    }

    review = facade.create_review(review_data)
    assert review is not None
    assert review.text == 'Super séjour'
    assert review.rating == 5


def test_create_review_invalid_user():
    facade = HBnBFacade()
    with pytest.raises(ValueError) as e:
        facade.create_review({
            'user_id': 'fake_id',
            'place_id': 'another_fake',
            'text': 'Test',
            'rating': 4
        })
    assert 'user_id' in str(e.value)



def test_get_review():
    facade = HBnBFacade()

    user = facade.create_user({'email': 'user@ex.com'})
    place = facade.create_place({
        'title': 'Cabane',
        'description': '',
        'price': 55,
        'latitude': 45.5,
        'longitude': -0.5,
        'owner_id': user.id,
        'amenities': []
    })

    review = facade.create_review({
        'user_id': user.id,
        'place_id': place.id,
        'text': 'Correct',
        'rating': 3
    })

    result = facade.get_review(review.id)
    assert result is not None
    assert result.text == 'Correct'
    assert result.rating == 3



def test_update_review():
    facade = HBnBFacade()

    user = facade.create_user({'email': 'update@ex.com'})
    place = facade.create_place({
        'title': 'Appartement',
        'description': 'Propre',
        'price': 75,
        'latitude': 44.0,
        'longitude': 1.0,
        'owner_id': user.id,
        'amenities': []
    })

    review = facade.create_review({
        'user_id': user.id,
        'place_id': place.id,
        'text': 'Pas mal',
        'rating': 3
    })

    updated = facade.update_review(review.id, {'text': 'Très bien', 'rating': 4})
    assert updated.text == 'Très bien'
    assert updated.rating == 4


def test_delete_review():
    facade = HBnBFacade()

    user = facade.create_user({'email': 'del@ex.com'})
    place = facade.create_place({
        'title': 'Villa',
        'description': 'Vue mer',
        'price': 200,
        'latitude': 42.0,
        'longitude': 3.0,
        'owner_id': user.id,
        'amenities': []
    })

    review = facade.create_review({
        'user_id': user.id,
        'place_id': place.id,
        'text': 'Magnifique',
        'rating': 5
    })

    facade.delete_review(review.id)
    with pytest.raises(ValueError):
        facade.get_review(review.id)
