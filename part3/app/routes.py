from flask import request, jsonify
from app import db
from app.models import User

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    user = User(username=username, email=email)
    user.set_password(password)  # 🔐 Hashing happens here

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201



auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200

    return jsonify({"error": "Invalid credentials"}), 401


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200


@bp.route("/users", methods=["POST"])
@jwt_required()
@admin_required()
def create_user():
    data = request.get_json()
    user = User(
        username=data["username"],
        email=data["email"],
        role=data.get("role", "user")
    )
    user.set_password(data["password"])
    user_repo.add(user)
    return jsonify(user.to_dict()), 201

@bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    users = user_repo.get_all()
    return jsonify([user.to_dict() for user in users])

@bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    user = user_repo.get_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())

@bp.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required()
@admin_required
def modify_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        user.set_password(password)
    if role:
        user.role = role

    db.session.commit()
    return jsonify(user.to_dict()), 200

@bp.route("/amenities", methods=["POST"])
@jwt_required()
@admin_required
def create_amenity():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Amenity name required"}), 400

    amenity = Amenity(name=name)
    db.session.add(amenity)
    db.session.commit()
    return jsonify(amenity.to_dict()), 201
