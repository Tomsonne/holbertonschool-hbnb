from app.models.base_model import BaseModel

class Amenity(BaseModel):
    _allowed_attrs = ['name']

    def __init__(self, name, **kwargs):
        super().__init__()

        # Applique les champs valides depuis kwargs
        for key in kwargs:
            if key in self._allowed_attrs:
                setattr(self, key, kwargs[key])
        
        # Champ obligatoire explicite (prioritaire sur kwargs)
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
