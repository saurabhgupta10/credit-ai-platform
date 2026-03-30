from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import Loan, db

loan_bp = Blueprint("loan", __name__)

# ========================
# EMI CALCULATOR
# ========================
def calculate_emi(principal, rate, tenure):
    monthly_rate = rate / (12 * 100)
    emi = principal * monthly_rate * (1 + monthly_rate)**tenure / ((1 + monthly_rate)**tenure - 1)
    return round(emi, 2)

# ========================
# APPLY LOAN
# ========================
@loan_bp.route("/apply-loan", methods=["POST"])
@jwt_required()
def apply_loan():
    try:
        current_user = get_jwt_identity()
        data = request.json

        income = float(data["income"])
        loan_amount = float(data["loan_amount"])
        cibil_score = int(data["cibil_score"])

        # AI logic
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

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ========================
# VIEW USER LOANS
# ========================
@loan_bp.route("/my-loans", methods=["GET"])
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