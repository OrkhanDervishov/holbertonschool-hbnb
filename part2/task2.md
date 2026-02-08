<h3>1. Files</h3>

```py
presentation/
 └── api/
      └── v1/
           └── users.py

business/
 ├── facade.py
 └── services/
      └── user_service.py
```

<h3>2. Business Logic Layer</h3>

```py
from business.models.user import User


class UserService:

    def __init__(self, repository):
        self.repository = repository
        self.collection = "users"

    # ---------------- CREATE ---------------- #

    def create(self, data):
        user = User(**data)
        self.repository.save(self.collection, user.id, user)
        return user

    # ---------------- GET ONE ---------------- #

    def get(self, user_id):
        return self.repository.get(self.collection, user_id)

    # ---------------- GET ALL ---------------- #

    def get_all(self):
        return self.repository.get_all(self.collection)

    # ---------------- UPDATE ---------------- #

    def update(self, user_id, data):
        user = self.get(user_id)

        if not user:
            return None

        user.update(data)
        self.repository.save(self.collection, user.id, user)

        return user
```

<h3>3. Facade Layer</h3>

```py
from business.services.user_service import UserService


class HBnBFacade:

    def __init__(self, repository):
        self.user_service = UserService(repository)

    # ---------- USER METHODS ---------- #

    def create_user(self, data):
        return self.user_service.create(data)

    def get_user(self, user_id):
        return self.user_service.get(user_id)

    def get_users(self):
        return self.user_service.get_all()

    def update_user(self, user_id, data):
        return self.user_service.update(user_id, data)
```

<h3>3. Flask-RESTX User API</h3>

```py
from flask import request
from flask_restx import Namespace, Resource, fields

api = Namespace("users", description="User operations")

facade = None   # Injected from app bootstrap


# ---------------- API MODELS ---------------- #

user_input = api.model("UserInput", {
    "email": fields.String(required=True),
    "password": fields.String(required=True),
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True)
})

user_update = api.model("UserUpdate", {
    "email": fields.String,
    "password": fields.String,
    "first_name": fields.String,
    "last_name": fields.String
})

user_output = api.model("UserOutput", {
    "id": fields.String,
    "email": fields.String,
    "first_name": fields.String,
    "last_name": fields.String,
    "created_at": fields.String,
    "updated_at": fields.String
})


# ---------------- HELPERS ---------------- #

def sanitize_user(user):
    """Remove password from response"""
    data = user.to_dict()
    data.pop("password", None)
    return data


# ---------------- ROUTES ---------------- #

@api.route("/")
class UserList(Resource):

    @api.expect(user_input)
    @api.response(201, "User created", user_output)
    def post(self):
        """Create new user"""

        data = request.json

        try:
            user = facade.create_user(data)
            return sanitize_user(user), 201

        except ValueError as e:
            return {"error": str(e)}, 400

    # ✅ YOU WERE ASKED TO IMPLEMENT THIS
    @api.response(200, "List of users", [user_output])
    def get(self):
        """Get all users"""

        users = facade.get_users()

        return [sanitize_user(u) for u in users], 200


@api.route("/<user_id>")
class UserResource(Resource):

    @api.response(200, "User found", user_output)
    @api.response(404, "User not found")
    def get(self, user_id):
        """Get user by ID"""

        user = facade.get_user(user_id)

        if not user:
            return {"error": "User not found"}, 404

        return sanitize_user(user), 200

    # ✅ YOU WERE ASKED TO IMPLEMENT THIS
    @api.expect(user_update)
    @api.response(200, "User updated", user_output)
    @api.response(404, "User not found")
    def put(self, user_id):
        """Update user"""

        data = request.json

        try:
            user = facade.update_user(user_id, data)

            if not user:
                return {"error": "User not found"}, 404

            return sanitize_user(user), 200

        except ValueError as e:
            return {"error": str(e)}, 400
```

<h3>5. Register Namespace</h3>

```py
from flask_restx import Api
from .users import api as users_ns, facade as users_facade


def init_api(app, facade_instance):

    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Backend API"
    )

    users_facade = facade_instance
    users_ns.facade = facade_instance

    api.add_namespace(users_ns, path="/api/v1/users")
```

<h3>6. Update app.py</h3>

```py
from flask import Flask
from business.facade import HBnBFacade
from persistence.in_memory_repository import InMemoryRepository
from presentation.api.v1 import init_api


def create_app(config_class):

    app = Flask(__name__)
    app.config.from_object(config_class)

    repo = InMemoryRepository()
    facade = HBnBFacade(repo)

    init_api(app, facade)

    return app
```
