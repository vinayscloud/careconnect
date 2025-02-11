import os
from flask import Blueprint, request, jsonify, render_template
import mysql.connector
import hashlib
import jwt
import datetime
from functools import wraps

auth_bp = Blueprint('auth', __name__)

# ------------------------------------------------------------------------------
# Database Configuration
# ------------------------------------------------------------------------------
DB_HOST = "database-1.cm1p8c8kitx3.us-east-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PASSWORD = "Clod123456789"
DB_NAME = "careconnect"

# ------------------------------------------------------------------------------
# Secret key for JWT
# If 'SECRET_KEY' is not set in the environment, fallback to "my_hardcoded_key_for_testing_only".
# In a production environment, you should set SECRET_KEY as an environment variable.
# ------------------------------------------------------------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "my_hardcoded_key_for_testing_only")
print("Using SECRET_KEY:", SECRET_KEY)

def create_connection():
    print("[DEBUG] Attempting database connection...")
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print("[DEBUG] Database connection successful")
        return conn
    except mysql.connector.Error as e:
        print(f"[ERROR] Database connection failed: {e}")
        return None

def hash_password(password):
    print("[DEBUG] Hashing password")
    return hashlib.sha256(password.encode()).hexdigest()

def generate_jwt(user_id, username, role):
    """Generates a JWT token with user details."""
    payload = {
        "id": user_id,
        "username": username,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def token_required(f):
    """Decorator to protect routes requiring authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            # If token has "Bearer " prefix, split it out
            token = token.split("Bearer ")[-1]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = data  # Attach user details to the request
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated

# ------------------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------------------

# Login Page
@auth_bp.route("/login")
def login_page():
    print("[DEBUG] Rendering login page")
    return render_template('login.html')

# Login API
@auth_bp.route("/login", methods=["POST"])
def login_user():
    print("[DEBUG] Received login request")
    data = request.json
    print(f"[DEBUG] Login data received: {data}")

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        print("[ERROR] Missing email or password")
        return jsonify({"error": "Missing required fields"}), 400

    conn = create_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        print(f"[DEBUG] Checking user in database with email: {email}")

        cursor.execute("""
            SELECT id, username, role FROM users WHERE email = %s AND password = %s
        """, (email, hashed_password))
        user = cursor.fetchone()

        if user:
            user_id, username, role = user
            print(f"[DEBUG] Login successful for user: {username}")

            token = generate_jwt(user_id, username, role)

            return jsonify({
                "message": "Login successful",
                "token": token,
                "user": {"id": user_id, "username": username, "role": role}
            }), 200
        else:
            print("[ERROR] Invalid login credentials")
            return jsonify({"error": "Invalid credentials"}), 401
    except mysql.connector.Error as e:
        print(f"[ERROR] Database error during login: {e}")
        return jsonify({"error": f"Database error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

# Register API
@auth_bp.route("/register", methods=["POST"])
def register_user():
    print("[DEBUG] Received registration request")
    data = request.json
    print(f"[DEBUG] Registration data received: {data}")

    username = data.get("username")
    email = data.get("email")
    role = data.get("role")
    password = data.get("password")

    if not username or not email or not password:
        print("[ERROR] Missing username, email, or password")
        return jsonify({"error": "Missing required fields"}), 400

    conn = create_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        print(f"[DEBUG] Registering user: {username}, Email: {email}")

        cursor.execute("""
            INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)
        """, (username, email, hashed_password, role))
        conn.commit()

        print(f"[DEBUG] User {username} registered successfully")
        return jsonify({"message": "User registered successfully"}), 201
    except mysql.connector.Error as e:
        print(f"[ERROR] Database error during registration: {e}")
        return jsonify({"error": f"Database error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

# Protected Route Example
@auth_bp.route("/protected", methods=["GET"])
@token_required
def protected_route():
    """Example of a protected route requiring JWT authentication."""
    user = request.user
    return jsonify({"message": "You have access!", "user": user})

# Register Page
@auth_bp.route("/register_page")
def register_page():
    print("[DEBUG] Rendering register page")
    return render_template('register.html')
