<h3>1. cURL Testing Examples</h3>

Create User
```
curl -X POST http://localhost:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{
"email":"test@mail.com",
"first_name":"John",
"last_name":"Doe"
}'
```

```
201 Created
```

Create Amenity
```
curl -X POST http://localhost:5000/api/v1/amenities/ \
-H "Content-Type: application/json" \
-d '{"name":"WiFi"}'
```

```
201 Created
```

Create Place
```
curl -X POST http://localhost:5000/api/v1/places/ \
-H "Content-Type: application/json" \
-d '{
"title":"Nice Apartment",
"price":100,
"latitude":45,
"longitude":9,
"owner_id":"USER_ID"
}'
```

```
201 Created
```

Review Test
```
curl -X POST http://localhost:5000/api/v1/reviews/ \
-H "Content-Type: application/json" \
-d '{
"text":"Amazing stay",
"rating":5,
"user_id":"USER_ID",
"place_id":"PLACE_ID"
}'
```

```
201 Created
```

Delete Review
```
curl -X DELETE http://localhost:5000/api/v1/reviews/REVIEW_ID
```

```
200 OK
```

<h3>1. Unit Testing (pytest Example)</h3>

```
pip install pytest
```

```py
def test_create_review(client):

    payload = {
        "text": "Good",
        "rating": 4,
        "user_id": "test-user",
        "place_id": "test-place"
    }

    response = client.post("/api/v1/reviews/", json=payload)

    assert response.status_code == 201
    assert response.json["text"] == "Good"
```

```py
def test_invalid_rating(client):

    payload = {
        "text": "Bad",
        "rating": 10,
        "user_id": "test-user",
        "place_id": "test-place"
    }

    response = client.post("/api/v1/reviews/", json=payload)

    assert response.status_code == 400
```
