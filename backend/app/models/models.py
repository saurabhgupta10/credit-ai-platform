from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(50), default="user")


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    income = db.Column(db.Float)
    loan_amount = db.Column(db.Float)
    cibil_score = db.Column(db.Integer)
    status = db.Column(db.String(50))
    emi = db.Column(db.Float)
    tenure = db.Column(db.Integer)