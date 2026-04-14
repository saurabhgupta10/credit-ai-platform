from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.models.models import db


def create_app():
    print ("step 1 :Creating Flask app...")
    app = Flask(__name__)

    

    # ========================
    # CONFIGURATION
    # ========================
    print ("step 2 :Configuring app...")

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///creditai.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "supersecretkey"

    # ========================
    # INIT EXTENSIONS
    # ========================
    print ("step 3 :Initializing extensions DB...")

    db.init_app(app)
    
    print ("step 4 :Initializing extensions JWT+cors..")
    JWTManager(app)
    CORS(app)

    print ("step 5 :Importing routes...")
    from app.routes.auth_routes import auth_bp
    from app.routes.loan_routes import loan_bp
    from app.routes.admin_routes import admin_bp

    
    # ========================
    # REGISTER ROUTES
    # ========================
    print ("step 6:Registering blueprints of routes..")
    app.register_blueprint(auth_bp)
    app.register_blueprint(loan_bp)
    app.register_blueprint(admin_bp)
 
    # ========================
    # CREATE DATABASE
    # ========================
    print ("step 7 :Creating database tables if not exist...")
    with app.app_context():
        db.create_all()

    # ========================
    # HOME ROUTE
    # ========================
    @app.route("/")
    def home():
        return {"message": "CreditAI Backend Running Successfully!"}
    print ("step 8 :App creation completed, returning app instance...")

    return app