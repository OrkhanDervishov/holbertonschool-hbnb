<h3>1. Files</h3>

```py
business/services/amenity_service.py
business/facade.py
presentation/api/v1/amenities.py
presentation/api/v1/__init__.py
```

<h3>2. Business Logic Layer</h3>

```py
from business.models.amenity import Amenity


class AmenityService:

    def __init__(self, repository):
        self.repository = repository
        self.collection = "amenities"

    # ---------- CREATE ---------- #

    def create(self, data):
        amenity = Amenity(**data)
        self.repository.save(self.collection, amenity.id, amenity)
        return amenity

    # ---------- GET ONE ---------- #

    def get(self, amenity_id):
        return self.repository.get(self.collection, amenity_id)

    # ---------- GET ALL ---------- #

    def get_all(self):
        return self.repository.get_all(self.collection)

    # ---------- UPDATE ---------- #

    def update(self, amenity_id, data):
        amenity = self.get(amenity_id)

        if not amenity:
            return None

        amenity.update(data)
        self.repository.save(self.collection, amenity.id, amenity)

        return amenity
```

<h3>3. Facade Integration</h3>

```py
from business.services.user_service import UserService
from business.services.amenity_service import AmenityService


class HBnBFacade:

    def __init__(self, repository):
        self.user_service = UserService(repository)
        self.amenity_service = AmenityService(repository)

    # ---------- USER ---------- #

    def create_user(self, data):
        return self.user_service.create(data)

    def get_user(self, user_id):
        return self.user_service.get(user_id)

    def get_users(self):
        return self.user_service.get_all()

    def update_user(self, user_id, data):
        return self.user_service.update(user_id, data)

    # ---------- AMENITY ---------- #

    def create_amenity(self, data):
        return self.amenity_service.create(data)

    def get_amenity(self, amenity_id):
        return self.amenity_service.get(amenity_id)

    def get_amenities(self):
        return self.amenity_service.get_all()

    def update_amenity(self, amenity_id, data):
        return self.amenity_service.update(amenity_id, data)
```

<h3>4. Amenity API</h3>

```py
from flask import request
from flask_restx import Namespace, Resource, fields

api = Namespace("amenities", description="Amenity operations")

facade = None


# ---------- API MODELS ---------- #

amenity_input = api.model("AmenityInput", {
    "name": fields.String(required=True)
})

amenity_update = api.model("AmenityUpdate", {
    "name": fields.String
})

amenity_output = api.model("AmenityOutput", {
    "id": fields.String,
    "name": fields.String,
    "created_at": fields.String,
    "updated_at": fields.String
})


# ---------- ROUTES ---------- #

@api.route("/")
class AmenityList(Resource):

    @api.expect(amenity_input)
    @api.response(201, "Amenity created", amenity_output)
    def post(self):
        """Create amenity"""

        data = request.json

        try:
            amenity = facade.create_amenity(data)
            return amenity.to_dict(), 201

        except ValueError as e:
            return {"error": str(e)}, 400


    @api.response(200, "List of amenities", [amenity_output])
    def get(self):
        """Get all amenities"""

        amenities = facade.get_amenities()
        return [a.to_dict() for a in amenities], 200


@api.route("/<amenity_id>")
class AmenityResource(Resource):

    @api.response(200, "Amenity found", amenity_output)
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        """Get amenity by ID"""

        amenity = facade.get_amenity(amenity_id)

        if not amenity:
            return {"error": "Amenity not found"}, 404

        return amenity.to_dict(), 200


    @api.expect(amenity_update)
    @api.response(200, "Amenity updated", amenity_output)
    @api.response(404, "Amenity not found")
    def put(self, amenity_id):
        """Update amenity"""

        data = request.json

        try:
            amenity = facade.update_amenity(amenity_id, data)

            if not amenity:
                return {"error": "Amenity not found"}, 404

            return amenity.to_dict(), 200

        except ValueError as e:
            return {"error": str(e)}, 400
```

<h3>1. Register Namespace</h3>

```py
from flask_restx import Api
from .users import api as users_ns
from .amenities import api as amenities_ns


def init_api(app, facade):

    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Backend API"
    )

    users_ns.facade = facade
    amenities_ns.facade = facade

    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
```
