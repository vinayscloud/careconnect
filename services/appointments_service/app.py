from flask import Flask
from flask_cors import CORS
from routes import doctors_bp

app = Flask(__name__)
CORS(app)

# Register Blueprint
app.register_blueprint(doctors_bp, url_prefix="/api/doctors")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
