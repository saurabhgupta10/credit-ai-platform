from flask import Blueprint, request, jsonify
from app.models.models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

# ========================
# REGISTER
# ========================
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    # Check if email already exists
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"message": "Email already registered"}), 400

    # Hash password
    hashed_password = generate_password_hash(data["password"])

    # Get role (default user)
    role = data.get("role", "user")

    new_user = User(
        name=data["name"],
        email=data["email"],
        password=hashed_password,
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User Registered Successfully"})


# ========================
# LOGIN
# ========================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(email=data["email"]).first()

    # Check password
    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Invalid Credentials"}), 401

    access_token = create_access_token(identity=user.id)

    return jsonify({
        "message": "Login Successful",
        "token": access_token
    })