from flask import Flask
from flask_cors import CORS
from routes import auth_bp

app = Flask(__name__)
CORS(app)  # Enable CORS to allow communication with other services

# Register the authentication blueprint
app.register_blueprint(auth_bp, url_prefix="/api/auth")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)  # Run the auth service on port 5005




