import os
from flask import Flask, render_template
from flask_cors import CORS
from app.config import Config
from app.database import db
from flask_jwt_extended import JWTManager

# ✅ Corrected Blueprints Import
from app.routes.doctors import doctor_bp
from app.routes.appointments import appointment_bp
from app.routes.auth import auth_bp  # ✅ Correct Import (Was `routes`)

def create_app():
    # ✅ Get Frontend Path (Ensures Flask Loads HTML Pages)
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/pages"))

    # ✅ Initialize Flask App with Custom Template Folder
    app = Flask(__name__, template_folder=frontend_path, static_folder="../../frontend/assets")

    # ✅ Load Configuration
    app.config.from_object(Config)
    CORS(app)

    # ✅ Initialize Database & JWT
    db.init_app(app)
    jwt = JWTManager(app)

    # ✅ Register Blueprints (API Endpoints)
    app.register_blueprint(auth_bp, url_prefix="/auth")  # ✅ Corrected
    app.register_blueprint(doctor_bp, url_prefix="/api/doctors")
    app.register_blueprint(appointment_bp, url_prefix="/api/appointments")

    # ✅ Serve HTML Pages
    @app.route("/")
    def index():
        return render_template("index.html")  # Home Page

    @app.route("/pages/<page_name>")
    def load_page(page_name):
        try:
            return render_template(f"{page_name}.html")  # Dynamically Load Pages
        except:
            return "Page not found", 404

    # ✅ Ensure Database Tables Exist
    with app.app_context():
        db.create_all()

    return app
