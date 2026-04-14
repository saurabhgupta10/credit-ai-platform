from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import User, Loan, db
from functools import wraps

admin_bp = Blueprint("admin", __name__)

# ========================
# ADMIN DECORATOR
# ========================
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
# VIEW ALL USERS
# ========================
@admin_bp.route("/all-users", methods=["GET"])
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
# VIEW ALL LOANS
# ========================
@admin_bp.route("/all-loans", methods=["GET"])
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
# UPDATE LOAN STATUS
# ========================
@admin_bp.route("/update-loan-status/<int:loan_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_loan_status(loan_id):
    data = request.json
    loan = Loan.query.get(loan_id)

    if not loan:
        return jsonify({"message": "Loan not found"}), 404

    loan.status = data["status"]
    db.session.commit()

    return jsonify({"message": "Loan status updated successfully"})

# ========================
# ADMIN DASHBOARD
# ========================
@admin_bp.route("/admin-dashboard", methods=["GET"])
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