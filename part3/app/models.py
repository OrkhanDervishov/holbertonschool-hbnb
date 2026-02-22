from app import db, bcrypt

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default="user")

    # Relationships
    places = db.relationship("Place", backref="owner", lazy=True, cascade="all, delete-orphan")
    reviews = db.relationship("Review", backref="author", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    def is_admin(self) -> bool:
        return self.role == "admin"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role
        }
    


class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email: str):
        return User.query.filter_by(email=email).first()

    def get_by_username(self, username: str):
        return User.query.filter_by(username=username).first()
    


class Place(db.Model):
    __tablename__ = "places"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=True)
    country = db.Column(db.String(120), nullable=False)
    price_per_night = db.Column(db.Float, nullable=False, default=0.0)
    max_guests = db.Column(db.Integer, nullable=False, default=1)
    number_of_rooms = db.Column(db.Integer, nullable=False, default=1)
    number_of_bathrooms = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # One-to-many: Place → Reviews
    reviews = db.relationship("Review", backref="place", lazy=True, cascade="all, delete-orphan")

    # Many-to-many: Place ↔ Amenity
    amenities = db.relationship(
        "Amenity",
        secondary="place_amenity",
        back_populates="places"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "price_per_night": self.price_per_night,
            "max_guests": self.max_guests,
            "number_of_rooms": self.number_of_rooms,
            "number_of_bathrooms": self.number_of_bathrooms,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }    


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey("places.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }    

class Amenity(db.Model):
    __tablename__ = "amenities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Many-to-many: Amenity ↔ Place
    places = db.relationship(
        "Place",
        secondary="place_amenity",
        back_populates="amenities"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }