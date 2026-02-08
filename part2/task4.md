<h3>1. Files</h3>

```py
business/services/place_service.py
business/facade.py
presentation/api/v1/places.py
presentation/api/v1/__init__.py
```

<h3>2. Business Logic Layer</h3>

```py
from business.models.place import Place


class PlaceService:

    def __init__(self, repository):
        self.repository = repository
        self.collection = "places"

    # ---------- CREATE ---------- #

    def create(self, data, user_service, amenity_service):

        owner = user_service.get(data["owner_id"])
        if not owner:
            raise ValueError("Owner not found")

        amenities = []
        amenity_ids = data.get("amenity_ids", [])

        for aid in amenity_ids:
            amenity = amenity_service.get(aid)
            if not amenity:
                raise ValueError(f"Amenity {aid} not found")
            amenities.append(amenity)

        place = Place(
            title=data["title"],
            description=data.get("description"),
            price=data["price"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            owner=owner,
            amenities=amenities
        )

        self.repository.save(self.collection, place.id, place)
        return place

    # ---------- GET ONE ---------- #

    def get(self, place_id):
        return self.repository.get(self.collection, place_id)

    # ---------- GET ALL ---------- #

    def get_all(self):
        return self.repository.get_all(self.collection)

    # ---------- UPDATE ---------- #

    def update(self, place_id, data, amenity_service):

        place = self.get(place_id)
        if not place:
            return None

        place.update(data)

        if "amenity_ids" in data:
            new_amenities = []
            for aid in data["amenity_ids"]:
                amenity = amenity_service.get(aid)
                if not amenity:
                    raise ValueError(f"Amenity {aid} not found")
                new_amenities.append(amenity)

            place.amenities = new_amenities

        self.repository.save(self.collection, place.id, place)
        return place
```

<h3>3. Facade Integration</h3>

```py
from business.services.user_service import UserService
from business.services.amenity_service import AmenityService
from business.services.place_service import PlaceService


class HBnBFacade:

    def __init__(self, repository):
        self.user_service = UserService(repository)
        self.amenity_service = AmenityService(repository)
        self.place_service = PlaceService(repository)

    # ---------- PLACE ---------- #

    def create_place(self, data):
        return self.place_service.create(
            data,
            self.user_service,
            self.amenity_service
        )

    def get_place(self, place_id):
        return self.place_service.get(place_id)

    def get_places(self):
        return self.place_service.get_all()

    def update_place(self, place_id, data):
        return self.place_service.update(
            place_id,
            data,
            self.amenity_service
        )

```

<h3>4. Place API</h3>

```py
from flask import request
from flask_restx import Namespace, Resource, fields

api = Namespace("places", description="Place operations")

facade = None


# ---------- API MODELS ---------- #

place_input = api.model("PlaceInput", {
    "title": fields.String(required=True),
    "description": fields.String,
    "price": fields.Float(required=True),
    "latitude": fields.Float(required=True),
    "longitude": fields.Float(required=True),
    "owner_id": fields.String(required=True),
    "amenity_ids": fields.List(fields.String)
})

place_update = api.model("PlaceUpdate", {
    "title": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "latitude": fields.Float,
    "longitude": fields.Float,
    "amenity_ids": fields.List(fields.String)
})

place_output = api.model("PlaceOutput", {
    "id": fields.String,
    "title": fields.String,
    "description": fields.String,
    "price": fields.Float,
    "latitude": fields.Float,
    "longitude": fields.Float,
    "owner_id": fields.String,
    "amenities": fields.List(fields.String),
    "created_at": fields.String,
    "updated_at": fields.String
})
```

<h3>5. Register Namespace</h3>

```py
from flask_restx import Api
from .users import api as users_ns
from .amenities import api as amenities_ns
from .places import api as places_ns


def init_api(app, facade):

    api = Api(app)

    users_ns.facade = facade
    amenities_ns.facade = facade
    places_ns.facade = facade

    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(places_ns, path="/api/v1/places")
```
