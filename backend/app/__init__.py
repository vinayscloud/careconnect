import os
from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.database import db

def create_app():
    # Initialize Flask App
    app = Flask(__name__)
    
    # Get the absolute path of the frontend folder
    # frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/pages"))

    # Set Configurations
    app.config.from_object(Config)
    CORS(app)  # Enable CORS for frontend

    # Initialize Database
    db.init_app(app)

    # Register Blueprints
    from app.routes.doctors import doctor_bp
    from app.routes.appointments import appointment_bp
    from app.routes.auth import auth_bp
    from app.routes.admin_user import admin_user_bp 

    app.register_blueprint(doctor_bp, url_prefix='/api/doctors')
    app.register_blueprint(appointment_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_user_bp)
    return app
