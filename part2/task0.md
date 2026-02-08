<h3>1. Project Directory structure</h3>

```
hbnb/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── presentation/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── places.py
│   │   └── amenities.py
│
├── business/
│   ├── __init__.py
│   ├── facade.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── place_service.py
│   │   └── amenity_service.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   ├── user.py
│   │   ├── place.py
│   │   └── amenity.py
│
├── persistence/
│   ├── __init__.py
│   ├── repository.py
│   ├── in_memory_repository.py
│   └── database/
│       ├── __init__.py
│       └── base.py
│
└── utils/
    ├── __init__.py
    └── validators.py
```

<h3>2. Flask Entry Points</h3>

```py
from flask import Flask
from presentation.routes import register_routes
from business.facade import HBnBFacade
from persistence.in_memory_repository import InMemoryRepository

def create_app():
    app = Flask(__name__)

    # Initialize repository
    repository = InMemoryRepository()

    # Initialize facade
    facade = HBnBFacade(repository)

    # Register routes
    register_routes(app, facade)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
```

<h3>3. Presentation Layer</h3>

```py
from .users import users_bp
from .places import places_bp
from .amenities import amenities_bp

def register_routes(app, facade):
    users_bp.facade = facade
    places_bp.facade = facade
    amenities_bp.facade = facade

    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(places_bp, url_prefix="/places")
    app.register_blueprint(amenities_bp, url_prefix="/amenities")
```

<h3>4. Business Layer</h3>

```py
from business.services.user_service import UserService
from business.services.place_service import PlaceService
from business.services.amenity_service import AmenityService


class HBnBFacade:
    def __init__(self, repository):
        self.user_service = UserService(repository)
        self.place_service = PlaceService(repository)
        self.amenity_service = AmenityService(repository)

    # USER METHODS
    def create_user(self, data):
        return self.user_service.create(data)

    # PLACE METHODS
    def create_place(self, data):
        return self.place_service.create(data)

    # AMENITY METHODS
    def create_amenity(self, data):
        return self.amenity_service.create(data)
```

<h3>5. Business Model</h3>

```py
import uuid
from datetime import datetime


class BaseModel:
    def __init__(self, id=None, created_at=None, updated_at=None):
        self.id = id or str(uuid.uuid4())
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
```

<h3>6. Persistence Layer</h3>

```py
from abc import ABC, abstractmethod


class Repository(ABC):

    @abstractmethod
    def save(self, collection, obj_id, obj):
        pass

    @abstractmethod
    def get(self, collection, obj_id):
        pass

    @abstractmethod
    def get_all(self, collection):
        pass

    @abstractmethod
    def delete(self, collection, obj_id):
        pass
```

<h3>7. In-Memory Repository</h3>

```py
from persistence.repository import Repository


class InMemoryRepository(Repository):

    def __init__(self):
        self.storage = {}

    def _get_collection(self, collection):
        if collection not in self.storage:
            self.storage[collection] = {}
        return self.storage[collection]

    def save(self, collection, obj_id, obj):
        col = self._get_collection(collection)
        col[obj_id] = obj

    def get(self, collection, obj_id):
        col = self._get_collection(collection)
        return col.get(obj_id)

    def get_all(self, collection):
        col = self._get_collection(collection)
        return list(col.values())

    def delete(self, collection, obj_id):
        col = self._get_collection(collection)
        if obj_id in col:
            del col[obj_id]
```

<h3>8. Preparing for SQLAlchemy</h3>

```py
# Placeholder for SQLAlchemy base
# from sqlalchemy.orm import declarative_base
# Base = declarative_base()
```

<h3>9. Configuration File</h3>

```py
import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    "development": DevelopmentConfig,
    "default": DevelopmentConfig
}
```

<h3>10. Requirements</h3>

```py
flask
flask-restx
```

<h3>10. Requirements</h3>

```py
flask
flask-restx
```
