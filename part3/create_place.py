from app import create_app
from app.extensions import db
from app.models.place import Place
import uuid
from datetime import datetime, timezone

app = create_app()

with app.app_context():
    place = Place(title="Test Place")  # Ne passe que les champs que __init__ accepte

    # Assigne manuellement les autres champs
    place.id = str(uuid.uuid4())
    place.created_at = datetime.now(timezone.utc)
    place.updated_at = datetime.now(timezone.utc)

    # Ajoute d'autres champs obligatoires ici si ton modèle en exige (ex: owner_id, description, etc.)

    db.session.add(place)
    db.session.commit()

    print("✅ Place ajouté :", place.id)
