-- =====================================================
-- Initial Users
-- =====================================================

INSERT INTO users (username, email, password_hash, role)
VALUES 
('admin', 'admin@hbnb.com', '$2b$12$examplehashedpassword', 'admin'),
('john_doe', 'john@example.com', '$2b$12$examplehashedpassword', 'user'),
('jane_smith', 'jane@example.com', '$2b$12$examplehashedpassword', 'user');

-- =====================================================
-- Initial Places
-- =====================================================

INSERT INTO places (name, description, city, state, country, price_per_night, max_guests, number_of_rooms, number_of_bathrooms, user_id)
VALUES
('Cozy Cottage', 'A cozy cottage near the lake', 'Springfield', 'IL', 'USA', 120.0, 4, 2, 1, 2),
('Downtown Apartment', 'Modern apartment in city center', 'New York', 'NY', 'USA', 250.0, 2, 1, 1, 3);

-- =====================================================
-- Initial Reviews
-- =====================================================

INSERT INTO reviews (text, rating, user_id, place_id)
VALUES
('Great place, very clean!', 5, 3, 1),
('Excellent location, will come again', 4, 2, 2);

-- =====================================================
-- Initial Amenities
-- =====================================================

INSERT INTO amenities (name, description)
VALUES
('WiFi', 'High-speed wireless internet'),
('Pool', 'Outdoor swimming pool'),
('Air Conditioning', 'Central air conditioning');

-- =====================================================
-- Assign Amenities to Places (many-to-many)
-- =====================================================

INSERT INTO place_amenity (place_id, amenity_id)
VALUES
(1, 1), -- Cozy Cottage has WiFi
(1, 3), -- Cozy Cottage has Air Conditioning
(2, 1), -- Downtown Apartment has WiFi
(2, 3); -- Downtown Apartment has Air Conditioning