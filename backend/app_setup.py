from flask import Flask, render_template
from flask_cors import CORS
from app.routes.doctors import doctors_bp
from app.routes.appointments import appointments_bp
from app.routes.auth import auth_bp
from app.routes.admin_user import admin_user_bp
from app.routes.view_doctor_appointments import doctor_view_appointments_bp
def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__, template_folder="../frontend/pages", static_folder="../frontend/assets")

    # ✅ Enable CORS (Cross-Origin Resource Sharing)
    CORS(app)

    # ✅ Register API Blueprints (Routes)
    app.register_blueprint(doctors_bp, url_prefix="/api/doctors")
    app.register_blueprint(appointments_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_user_bp)
    app.register_blueprint(doctor_view_appointments_bp)
    # ✅ Serve Frontend Pages
    @app.route('/')
    def index():
        return render_template("index.html")  # Default page

    # ✅ Dynamic Route to Load Any HTML File
    @app.route('/pages/<page_name>')
    def load_page(page_name):
        try:
            return render_template(f"{page_name}.html")  # Load requested HTML file
        except:
            return "Page not found", 404

    # ✅ Set Secret Key
    app.secret_key = "d28ab6f8995286e60aed281a574c18a03ff99490de1ab1f6"

    return app
