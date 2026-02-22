erDiagram
    USERS {
        INT id PK
        VARCHAR username UNIQUE
        VARCHAR email UNIQUE
        VARCHAR password_hash
        VARCHAR role
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    PLACES {
        INT id PK
        VARCHAR name
        TEXT description
        VARCHAR city
        VARCHAR state
        VARCHAR country
        FLOAT price_per_night
        INT max_guests
        INT number_of_rooms
        INT number_of_bathrooms
        INT user_id FK
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    REVIEWS {
        INT id PK
        TEXT text
        INT rating
        INT user_id FK
        INT place_id FK
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    AMENITIES {
        INT id PK
        VARCHAR name UNIQUE
        TEXT description
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    PLACE_AMENITY {
        INT place_id PK FK
        INT amenity_id PK FK
    }

    %% Relationships
    USERS ||--o{ PLACES : "owns"
    USERS ||--o{ REVIEWS : "writes"
    PLACES ||--o{ REVIEWS : "receives"
    PLACES ||--o{ PLACE_AMENITY : "has"
    AMENITIES ||--o{ PLACE_AMENITY : "included in"