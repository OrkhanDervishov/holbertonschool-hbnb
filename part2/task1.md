<h3>1. Business Model Folder</h3>

```py
business/models/
│
├── base_model.py
├── user.py
├── place.py
├── review.py
├── amenity.py
└── __init__.py
```

<h3>2. Base Model</h3>

```py
import uuid
from datetime import datetime


class BaseModel:
    """Base class for all models"""

    def __init__(self, id=None, created_at=None, updated_at=None):
        self.id = id or str(uuid.uuid4())
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def update_timestamp(self):
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
```

<h3>3. User Model</h3>

```py
from business.models.base_model import BaseModel


class User(BaseModel):

    def __init__(self, email, password, first_name, last_name, **kwargs):
        super().__init__(**kwargs)

        self.set_email(email)
        self.set_password(password)
        self.set_first_name(first_name)
        self.set_last_name(last_name)

        self.places = []      # Places owned by user
        self.reviews = []     # Reviews written by user

    # ---------------- Validation ---------------- #

    def set_email(self, email):
        if not email or "@" not in email:
            raise ValueError("Invalid email")
        self.email = email.lower()

    def set_password(self, password):
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        self.password = password

    def set_first_name(self, name):
        if not name:
            raise ValueError("First name required")
        self.first_name = name

    def set_last_name(self, name):
        if not name:
            raise ValueError("Last name required")
        self.last_name = name

    # ---------------- Update ---------------- #

    def update(self, data):
        if "email" in data:
            self.set_email(data["email"])
        if "password" in data:
            self.set_password(data["password"])
        if "first_name" in data:
            self.set_first_name(data["first_name"])
        if "last_name" in data:
            self.set_last_name(data["last_name"])

        self.update_timestamp()

    # ---------------- Serialization ---------------- #

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "places": [p.id for p in self.places],
            "reviews": [r.id for r in self.reviews]
        })
        return base
```

<h3>4. Amenity Model</h3>

```py
from business.models.base_model import BaseModel


class Amenity(BaseModel):

    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.set_name(name)

    def set_name(self, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Amenity name required")
        self.name = name.strip()

    def update(self, data):
        if "name" in data:
            self.set_name(data["name"])
        self.update_timestamp()

    def to_dict(self):
        base = super().to_dict()
        base["name"] = self.name
        return base
```

<h3>5. Place Model</h3>

```py
from business.models.base_model import BaseModel


class Place(BaseModel):

    def __init__(
        self,
        title,
        description,
        price,
        latitude,
        longitude,
        owner,
        amenities=None,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.set_title(title)
        self.set_description(description)
        self.set_price(price)
        self.set_latitude(latitude)
        self.set_longitude(longitude)

        self.owner = owner
        self.reviews = []
        self.amenities = amenities or []

        owner.places.append(self)

    # ---------------- Validation ---------------- #

    def set_title(self, title):
        if not title:
            raise ValueError("Title required")
        self.title = title

    def set_description(self, description):
        self.description = description or ""

    def set_price(self, price):
        if price < 0:
            raise ValueError("Price must be positive")
        self.price = float(price)

    def set_latitude(self, lat):
        if not (-90 <= lat <= 90):
            raise ValueError("Invalid latitude")
        self.latitude = lat

    def set_longitude(self, lng):
        if not (-180 <= lng <= 180):
            raise ValueError("Invalid longitude")
        self.longitude = lng

    # ---------------- Amenity Handling ---------------- #

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    # ---------------- Update ---------------- #

    def update(self, data):
        if "title" in data:
            self.set_title(data["title"])
        if "description" in data:
            self.set_description(data["description"])
        if "price" in data:
            self.set_price(data["price"])

        self.update_timestamp()

    # ---------------- Serialization ---------------- #

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner.id,
            "amenities": [a.id for a in self.amenities],
            "reviews": [r.id for r in self.reviews]
        })
        return base
```
<h3>6. Review Model</h3>

```py
from business.models.base_model import BaseModel


class Review(BaseModel):

    def __init__(self, text, rating, user, place, **kwargs):
        super().__init__(**kwargs)

        self.set_text(text)
        self.set_rating(rating)

        self.user = user
        self.place = place

        user.reviews.append(self)
        place.reviews.append(self)

    # ---------------- Validation ---------------- #

    def set_text(self, text):
        if not text:
            raise ValueError("Review text required")
        self.text = text

    def set_rating(self, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be 1-5")
        self.rating = int(rating)

    # ---------------- Update ---------------- #

    def update(self, data):
        if "text" in data:
            self.set_text(data["text"])
        if "rating" in data:
            self.set_rating(data["rating"])

        self.update_timestamp()

    # ---------------- Serialization ---------------- #

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user.id,
            "place_id": self.place.id
        })
        return base
```
