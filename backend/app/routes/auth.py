from flask import Blueprint, request, jsonify, render_template
import mysql.connector
import hashlib

auth_bp = Blueprint('auth', __name__)

# Database Configuration
DB_HOST = "database-1.cm1p8c8kitx3.us-east-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PASSWORD = "Clod123456789"
DB_NAME = "careconnect"

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
            SELECT id, username FROM users WHERE email = %s AND password = %s
        """, (email, hashed_password))
        user = cursor.fetchone()

        if user:
            print(f"[DEBUG] Login successful for user: {user[1]}")
            return jsonify({"message": "Login successful", "user": {"id": user[0], "username": user[1]}}), 200
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
            INSERT INTO users (username, email, password) VALUES (%s, %s, %s)
        """, (username, email, hashed_password))
        conn.commit()

        print(f"[DEBUG] User {username} registered successfully")
        return jsonify({"message": "User registered successfully"}), 201
    except mysql.connector.Error as e:
        print(f"[ERROR] Database error during registration: {e}")
        return jsonify({"error": f"Database error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

# Register Page
@auth_bp.route("/register_page")
def register_page():
    print("[DEBUG] Rendering register page")
    return render_template('register.html')


