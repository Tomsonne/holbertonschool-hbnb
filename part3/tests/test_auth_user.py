import json
from flask_jwt_extended import create_access_token

def get_headers(token=None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return headers

def test_login_successful(client, admin_user):
    """Test login with valid credentials"""
    res = client.post(
        '/api/v1/auth/login',
        headers=get_headers(),
        data=json.dumps({
            "email": admin_user["email"],
            "password": admin_user["password"]
        })
    )
    assert res.status_code == 200
    data = res.get_json()
    assert 'access_token' in data

def test_login_failure(client):
    """Test login with wrong credentials"""
    res = client.post(
        '/api/v1/auth/login',
        headers=get_headers(),
        data=json.dumps({
            "email": "fake@example.com",
            "password": "wrongpass"
        })
    )
    assert res.status_code == 401

def test_create_user_as_admin(client, admin_user):
    """Test that admin can create a user"""
    # crée un token JWT avec l'ID et le flag admin du fixture
    token = create_access_token(identity=json.dumps({
        "id": admin_user["id"],
        "is_admin": admin_user["is_admin"]
    }))
    res = client.post(
        '/api/v1/users',
        headers=get_headers(token),
        data=json.dumps({
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
            "password": "pass123"
        })
    )
    assert res.status_code == 201
    assert res.get_json()['email'] == "alice@example.com"

def test_create_user_as_non_admin(client, normal_user):
    """Test that non-admin cannot create a user"""
    token = create_access_token(identity=json.dumps({
        "id": normal_user["id"],
        "is_admin": normal_user["is_admin"]
    }))
    res = client.post(
        '/api/v1/users',
        headers=get_headers(token),
        data=json.dumps({
            "first_name": "Bob",
            "last_name": "Doe",
            "email": "bob@example.com",
            "password": "pass456"
        })
    )
    assert res.status_code == 403

def test_get_users_as_admin(client, admin_user):
    """Test that admin can list users"""
    token = create_access_token(identity=json.dumps({
        "id": admin_user["id"],
        "is_admin": admin_user["is_admin"]
    }))
    res = client.get('/api/v1/users', headers=get_headers(token))
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)

def test_get_users_as_non_admin(client, normal_user):
    """Test that non-admin cannot list users"""
    token = create_access_token(identity=json.dumps({
        "id": normal_user["id"],
        "is_admin": normal_user["is_admin"]
    }))
    res = client.get('/api/v1/users', headers=get_headers(token))
    assert res.status_code == 403
