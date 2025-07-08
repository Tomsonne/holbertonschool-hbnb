import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db
from app.services import facade


@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def admin_user(app):
    with app.app_context():
        u = facade.create_user({
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@example.com",
            "password": "adminpass",
            "is_admin": True
        })
        db.session.refresh(u)  # rebinde l'utilisateur
        return {
            "id": str(u.id),
            "email": u.email,
            "password": "adminpass",
            "is_admin": True
        }


@pytest.fixture()
def normal_user(app):
    with app.app_context():
        u = facade.create_user({
            "first_name": "Normal",
            "last_name": "User",
            "email": "user@example.com",
            "password": "userpass",
            "is_admin": False
        })
        db.session.refresh(u)
        return {
            "id": str(u.id),
            "email": u.email,
            "password": "userpass",
            "is_admin": False
        }

@pytest.fixture(autouse=True)
def clean_database(app):
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
