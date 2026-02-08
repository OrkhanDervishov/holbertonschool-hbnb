<h3>1. Files</h3>

```py
business/services/review_service.py
business/facade.py
presentation/api/v1/reviews.py
presentation/api/v1/places.py (update)
presentation/api/v1/__init__.py (register namespace)
```

<h3>2. Business Logic — Review Service</h3>

```py
from business.models.review import Review


class ReviewService:

    def __init__(self, repository):
        self.repository = repository
        self.collection = "reviews"

    # ---------- CREATE ---------- #

    def create(self, data, user_service, place_service):

        user = user_service.get(data["user_id"])
        if not user:
            raise ValueError("User not found")

        place = place_service.get(data["place_id"])
        if not place:
            raise ValueError("Place not found")

        review = Review(
            text=data["text"],
            rating=data["rating"],
            user=user,
            place=place
        )

        self.repository.save(self.collection, review.id, review)
        return review

    # ---------- GET ---------- #

    def get(self, review_id):
        return self.repository.get(self.collection, review_id)

    def get_all(self):
        return self.repository.get_all(self.collection)

    # ---------- GET BY PLACE ---------- #

    def get_by_place(self, place_id):
        reviews = self.get_all()
        return [r for r in reviews if r.place.id == place_id]

    # ---------- UPDATE ---------- #

    def update(self, review_id, data):

        review = self.get(review_id)
        if not review:
            return None

        review.update(data)
        self.repository.save(self.collection, review.id, review)

        return review

    # ---------- DELETE ---------- #

    def delete(self, review_id):

        review = self.get(review_id)
        if not review:
            return False

        # Remove relationships
        if review in review.user.reviews:
            review.user.reviews.remove(review)

        if review in review.place.reviews:
            review.place.reviews.remove(review)

        self.repository.delete(self.collection, review_id)
        return True
```

<h3>3. Facade Integration</h3>

```py
from business.services.review_service import ReviewService
```

```py
self.review_service = ReviewService(repository)
```

```py
# ---------- REVIEW ---------- #

def create_review(self, data):
    return self.review_service.create(
        data,
        self.user_service,
        self.place_service
    )

def get_review(self, review_id):
    return self.review_service.get(review_id)

def get_reviews(self):
    return self.review_service.get_all()

def get_reviews_by_place(self, place_id):
    return self.review_service.get_by_place(place_id)

def update_review(self, review_id, data):
    return self.review_service.update(review_id, data)

def delete_review(self, review_id):
    return self.review_service.delete(review_id)

```

<h3>4. Review API</h3>

```py
from flask import request
from flask_restx import Namespace, Resource, fields

api = Namespace("reviews", description="Review operations")

facade = None
```

API Models
```py
review_input = api.model("ReviewInput", {
    "text": fields.String(required=True),
    "rating": fields.Integer(required=True),
    "user_id": fields.String(required=True),
    "place_id": fields.String(required=True)
})

review_update = api.model("ReviewUpdate", {
    "text": fields.String,
    "rating": fields.Integer
})

review_output = api.model("ReviewOutput", {
    "id": fields.String,
    "text": fields.String,
    "rating": fields.Integer,
    "user_id": fields.String,
    "place_id": fields.String,
    "created_at": fields.String,
    "updated_at": fields.String
})
```

Serializer
```py
def serialize_review(review):
    data = review.to_dict()
    return data

```

Review List
```py
@api.route("/")
class ReviewList(Resource):

    @api.expect(review_input)
    def post(self):

        try:
            review = facade.create_review(request.json)
            return serialize_review(review), 201

        except ValueError as e:
            return {"error": str(e)}, 400


    def get(self):
        reviews = facade.get_reviews()
        return [serialize_review(r) for r in reviews], 200
```

Single Review
```py
@api.route("/<review_id>")
class ReviewResource(Resource):

    def get(self, review_id):

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        return serialize_review(review), 200


    @api.expect(review_update)
    def put(self, review_id):

        try:
            review = facade.update_review(review_id, request.json)

            if not review:
                return {"error": "Review not found"}, 404

            return serialize_review(review), 200

        except ValueError as e:
            return {"error": str(e)}, 400


    def delete(self, review_id):

        success = facade.delete_review(review_id)

        if not success:
            return {"error": "Review not found"}, 404

        return {"message": "Review deleted"}, 200
```

<h3>5. Update Places API → Add Reviews Endpoint</h3>

```py
@api.route("/<place_id>/reviews")
class PlaceReviews(Resource):

    def get(self, place_id):

        reviews = facade.get_reviews_by_place(place_id)
        return [r.to_dict() for r in reviews], 200

```

<h3>6. Register Namespace</h3>

```py
from .reviews import api as reviews_ns

reviews_ns.facade = facade
api.add_namespace(reviews_ns, path="/api/v1/reviews")
```
