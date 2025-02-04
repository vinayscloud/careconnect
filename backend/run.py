from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.database import db
from app.routes.auth import auth_bp
from app.config import Config

# ✅ Load from frontend pages & assets
app = Flask(__name__, template_folder="../frontend/pages", static_folder="../frontend/assets")

# ✅ Load Configuration
app.config.from_object(Config)
CORS(app)

# ✅ Initialize Database & JWT
db.init_app(app)
jwt = JWTManager(app)

# ✅ Register API Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")

# ✅ Serve Frontend Pages
@app.route("/")
def index():
    return render_template("index.html")  # Home Page

@app.route("/pages/<page_name>")
def load_page(page_name):
    try:
        return render_template(f"{page_name}.html")  # Load any requested HTML page dynamically
    except:
        return "Page not found", 404

# ✅ Create Tables if Not Exists
with app.app_context():
    db.create_all()

# ✅ Start Flask Server
if __name__ == "__main__":
    app.run(debug=True)
