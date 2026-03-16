# ========================
# IMPORTS
# ========================

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)
from flask_cors import CORS
import math

# ========================
# APP SETUP
# ========================

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///creditai.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "supersecretkey"

db = SQLAlchemy(app)
jwt = JWTManager(app)

# ========================
# ADMIN ACCESS DECORATOR
# ========================

from functools import wraps

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if user.role != "admin":
            return jsonify({"message": "Admin access required"}), 403

        return fn(*args, **kwargs)
    return wrapper

# ========================
# DATABASE MODELS
# ========================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))  # increased length for hash
    role = db.Column(db.String(50),default="user")

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    income = db.Column(db.Float)
    loan_amount = db.Column(db.Float)
    cibil_score = db.Column(db.Integer)
    status = db.Column(db.String(50))
    emi = db.Column(db.Float)
    tenure = db.Column(db.Integer)


# ========================
# CREATE DATABASE
# ========================

with app.app_context():
    db.create_all()

# ========================
# HOME ROUTE
# ========================

@app.route("/")
def home():
    return "🚀 CreditAI Backend Running Successfully!"

# ========================
# VIEW ALL USERS
# ========================

@app.route("/all-users")
@jwt_required()
@admin_required
def all_users():
    users = User.query.all()
    return jsonify([
        {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
        for user in users
    ])

# ========================
# ADMIN VIEW ALL LOANS
# ========================

@app.route("/all-loans")
@jwt_required()
@admin_required
def all_loans():

    loans = Loan.query.all()

    return jsonify([
        {
            "loan_id": loan.id,
            "user_id": loan.user_id,
            "loan_amount": loan.loan_amount,
            "status": loan.status
        }
        for loan in loans
    ])

# ========================
# ADMIN UPDATE LOAN STATUS
# ========================

@app.route("/update-loan-status/<int:loan_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_loan_status(loan_id):

    data = request.json
    loan = Loan.query.get(loan_id)

    if not loan:
        return jsonify({"message": "Loan not found"}), 404

    loan.status = data["status"]  # Approved / Rejected
    db.session.commit()

    return jsonify({"message": "Loan status updated successfully"})


# ========================
# REGISTER ROUTE (SECURE)
# ========================

@app.route("/register", methods=["POST"])
def register():

    data = request.json

    # Check if email already exists
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"message": "Email already registered"}), 400

    # 🔐 HASH PASSWORD
    hashed_password = generate_password_hash(data["password"])
    #GET ROLE (DEFAULT=USER)
    role=data.get("role","user")
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
# LOGIN ROUTE (SECURE)
# ========================

@app.route("/login", methods=["POST"])
def login():

    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    # 🔐 CHECK HASHED PASSWORD
    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Invalid Credentials"}), 401

    access_token = create_access_token(identity=user.id)

    return jsonify({
        "message": "Login Successful",
        "token": access_token
    })

# ========================
# EMI CALCULATOR FUNCTION
# ========================

def calculate_emi(principal, rate, tenure):
    monthly_rate = rate / (12 * 100)
    emi = principal * monthly_rate * (1 + monthly_rate)**tenure / ((1 + monthly_rate)**tenure - 1)
    return round(emi, 2)

# ========================
# APPLY LOAN
# ========================

@app.route("/apply-loan", methods=["POST"])
@jwt_required()
def apply_loan():

    current_user = get_jwt_identity()
    data = request.json

    income = float(data["income"])
    loan_amount = float(data["loan_amount"])
    cibil_score = int(data["cibil_score"])

    # Simple AI logic
    if cibil_score >= 700 and income >= loan_amount * 2:
        status = "Approved"
        interest_rate = 10
        tenure = 12
        emi = calculate_emi(loan_amount, interest_rate, tenure)
    else:
        status = "Rejected"
        emi = 0
        tenure = 0

    new_loan = Loan(
        user_id=current_user,
        income=income,
        loan_amount=loan_amount,
        cibil_score=cibil_score,
        status=status,
        emi=emi,
        tenure=tenure
    )

    db.session.add(new_loan)
    db.session.commit()

    return jsonify({
        "loan_status": status,
        "emi": emi,
        "tenure_months": tenure
    })

# ========================
# VIEW USER LOANS
# ========================

@app.route("/my-loans", methods=["GET"])
@jwt_required()
def my_loans():

    current_user = get_jwt_identity()
    loans = Loan.query.filter_by(user_id=current_user).all()

    result = []

    for loan in loans:
        result.append({
            "loan_amount": loan.loan_amount,
            "status": loan.status,
            "emi": loan.emi,
            "tenure": loan.tenure
        })

    return jsonify(result)


# ========================
# ADMIN DASHBOARD ANALYTICS
# ========================

@app.route("/admin-dashboard")
@jwt_required()
@admin_required
def admin_dashboard():

    total_users = User.query.count()
    total_loans = Loan.query.count()
    approved_loans = Loan.query.filter_by(status="Approved").count()
    rejected_loans = Loan.query.filter_by(status="Rejected").count()

    total_loan_amount = db.session.query(db.func.sum(Loan.loan_amount)).scalar() or 0

    approval_rate = 0
    if total_loans > 0:
        approval_rate = round((approved_loans / total_loans) * 100, 2)

    return jsonify({
        "total_users": total_users,
        "total_loans": total_loans,
        "approved_loans": approved_loans,
        "rejected_loans": rejected_loans,
        "total_loan_volume": total_loan_amount,
        "approval_rate_percent": approval_rate
    })

# ========================
# RUN SERVER
# ========================

if __name__ == "__main__":
    app.run(debug=True)