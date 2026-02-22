-- =====================================================
-- HBnB Database Schema
-- =====================================================

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(120) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Places table
CREATE TABLE places (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    description TEXT,
    city VARCHAR(120) NOT NULL,
    state VARCHAR(120),
    country VARCHAR(120) NOT NULL,
    price_per_night FLOAT DEFAULT 0.0 NOT NULL,
    max_guests INT DEFAULT 1 NOT NULL,
    number_of_rooms INT DEFAULT 1 NOT NULL,
    number_of_bathrooms INT DEFAULT 1 NOT NULL,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Reviews table
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT NOT NULL,
    user_id INT NOT NULL,
    place_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_review_user FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_review_place FOREIGN KEY(place_id) REFERENCES places(id) ON DELETE CASCADE
);

-- Amenities table
CREATE TABLE amenities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Association table for Place ↔ Amenity (many-to-many)
CREATE TABLE place_amenity (
    place_id INT NOT NULL,
    amenity_id INT NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    CONSTRAINT fk_pa_place FOREIGN KEY(place_id) REFERENCES places(id) ON DELETE CASCADE,
    CONSTRAINT fk_pa_amenity FOREIGN KEY(amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);