from flask import Flask, render_template
from flask_cors import CORS
from app.config import Config
from app.database import init_db, db
from app.routes.doctors import doctors_bp  # Import the doctors API route
from app.routes.appointments import appointments_bp  
from app.routes.auth import auth_bp 
from app.routes.admin_user import admin_user_bp 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# ✅ Initialize Flask App
app = Flask(__name__, template_folder="../frontend/pages", static_folder="../frontend/assets")

# ✅ Set Secret Key for Session Handling (Fixes Login Issue)
app.secret_key = "a3f9c1e2b47d8f56a9c0e3d7b21f45a6c8e0d9f3a2b4c6d7e8f9a0b1c2d3e4f5"

# ✅ Load Configuration
app.config.from_object(Config)

# ✅ Enable CORS (Cross-Origin Resource Sharing)
CORS(app)

# ✅ Initialize Database
init_db(app)

# ✅ Register API Blueprints (Routes)
app.register_blueprint(doctors_bp, url_prefix="/api/doctors")  # Example route
app.register_blueprint(appointments_bp) 
app.register_blueprint(auth_bp) 
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

# ✅ Serve Patient and Doctor Pages (Moved Above app.run())
@app.route('/patient.html')
def patient_dashboard():
    return render_template("patient.html")

@app.route('/doctor.html')
def doctor_dashboard():
    return render_template("doctor.html")

# ✅ Run the Flask App (No Routes After This)
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
