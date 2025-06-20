# 🏠 HBnB – Partie 2 : Implémentation de la logique métier et des endpoints API

## 📌 Présentation

Cette deuxième partie du projet **HBnB** vise à mettre en œuvre la **logique métier** et les **endpoints API** en s'appuyant sur la documentation technique rédigée précédemment.

Nous avons construit les couches **Business Logic** et **Presentation** à l’aide de **Python**, **Flask** et **flask-restx**, en respectant les principes d’architecture modulaire et de conception orientée objet. L’objectif est de poser les fondations robustes de l’application avant d’aborder les fonctionnalités avancées comme l’authentification JWT et les droits d’accès (prévu en partie 3).

---

## 🎯 Objectifs

- Structurer le projet selon une architecture modulaire (présentation, logique métier)
- Implémenter les entités principales : `User`, `Place`, `Review`, `Amenity`
- Appliquer le **pattern façade** pour simplifier les échanges entre les couches
- Créer des endpoints RESTful (CRUD) pour chaque entité
- Utiliser `flask-restx` pour organiser et documenter les routes
- Sérialiser les données et inclure des attributs étendus (ex : nom du propriétaire dans une ressource `Place`)
- Tester les endpoints avec `curl` et écrire des **tests unitaires**

---

## 🧱 Architecture

hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── base_model.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── facade.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   └── repository.py
│   └── tests/
│       ├── test_user.py
│       ├── test_place.py
│       ├── test_review.py
│       └── test_amenity.py
├── run.py
├── config.py
├── requirements.txt
└── README.md





---

## ⚙️ Technologies utilisées

- Python 3.11+
- Flask
- Flask-RESTX
- unittest
- curl / Postman
- PEP8 & conventions de projet Python
- Facade design pattern

---

## 📂 Endpoints API

Quelques exemples d'endpoints :

| Méthode | Endpoint              | Description                         |
|--------:|-----------------------|-------------------------------------|
| GET     | `/api/users`          | Récupérer tous les utilisateurs     |
| POST    | `/api/users`          | Créer un nouvel utilisateur         |
| GET     | `/api/places/<id>`    | Obtenir un lieu spécifique          |
| PUT     | `/api/reviews/<id>`   | Modifier un avis                    |
| DELETE  | `/api/amenities/<id>` | Supprimer une commodité             |

---

## 🧪 Exemple de test unitaire

Voici un extrait d’un test unitaire pour l'entité `User`, situé dans `app/tests/test_user.py` :

```python

import unittest
from app.models.user import User

class TestUserModel(unittest.TestCase):
    def test_user_initialization(self):
        user = User(first_name="Beydi", last_name="Sow", email="beydi@example.com")
        self.assertEqual(user.first_name, "Beydi")
        self.assertEqual(user.last_name, "Sow")
        self.assertEqual(user.email, "beydi@example.com")

    def test_user_string_representation(self):
        user = User(first_name="Beydi", last_name="Sow", email="beydi@example.com")
        self.assertIn("Beydi", str(user))

```

## 🧪 Lancement des tests

python3 -m unittest discover -s app/tests


## 🤝 Travail collaboratif

Projet réalisé en binôme dans le cadre de la formation **Holberton School**.

**Contributeurs** :
- [@Tomsonne](https://github.com/Tomsonne)
- [Nom ou GitHub du binôme ici]

---

## 📚 Ressources recommandées

- [Documentation Flask](https://flask.palletsprojects.com/)
- [Documentation flask-restx](https://flask-restx.readthedocs.io/)
- [RESTful API Design](https://restfulapi.net/)
- [PEP8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Pattern Façade – Refactoring.Guru](https://refactoring.guru/design-patterns/facade/python/example)

---

## 📌 Remarques

- L’authentification JWT et les rôles ne sont **pas implémentés ici**, mais la structure est prête à les accueillir en partie 3.
- Tous les tests sont à jour et couvrent les cas standards ainsi que plusieurs cas limites.
