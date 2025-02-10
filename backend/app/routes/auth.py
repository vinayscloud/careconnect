from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
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

# ✅ Login Page
@auth_bp.route("/login")
def login_page():
    print("[DEBUG] Rendering login page")
    return render_template('login.html')

# ✅ Login API (with Session Storage & Success Message)
# ✅ Login API (with Role-Based Redirection)
@auth_bp.route("/login", methods=["POST"])
def login_user():
    print("[DEBUG] Received login request")
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        print("[ERROR] Missing email or password")
        return jsonify({"error": "Missing required fields"}), 400

    conn = create_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        hashed_password = hash_password(password)
        print(f"[DEBUG] Checking user in database with email: {email}")

        cursor.execute("""
            SELECT id, username, role FROM users WHERE email = %s AND password = %s
        """, (email, hashed_password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role'].strip().lower()  # Ensure lowercase for consistency

            print(f"[DEBUG] Login successful for user: {user['username']} with role: {session['role']}")

            # ✅ Determine redirect based on role
            redirect_url = "/patient.html" if session['role'] == 'patient' else "/doctor.html"

            return jsonify({
                "message": "Login successful!",
                "username": user['username'],
                "redirect": redirect_url  # Send correct redirect URL
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


# ✅ Logout API (Clears Session)
@auth_bp.route("/logout", methods=["GET"])
def logout():
    print("[DEBUG] Logging out user")
    session.clear()
    return jsonify({"message": "Logged out successfully!"}), 200

# ✅ Register API (Restored)
@auth_bp.route("/register", methods=["POST"])
def register_user():
    print("[DEBUG] Received registration request")
    data = request.json
    print(f"[DEBUG] Registration data received: {data}")

    username = data.get("username")
    email = data.get("email")
    role = data.get("role")
    password = data.get("password")

    if not username or not email or not password or not role:
        print("[ERROR] Missing username, email, password, or role")
        return jsonify({"error": "Missing required fields"}), 400

    conn = create_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        print(f"[DEBUG] Registering user: {username}, Email: {email}, Role: {role}")

        cursor.execute("""
            INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)
        """, (username, email, hashed_password, role.lower()))  # Store role in lowercase
        conn.commit()

        print(f"[DEBUG] User {username} registered successfully")
        return jsonify({"message": "User registered successfully"}), 201
    except mysql.connector.Error as e:
        print(f"[ERROR] Database error during registration: {e}")
        return jsonify({"error": f"Database error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

# ✅ Register Page
@auth_bp.route("/register_page")
def register_page():
    print("[DEBUG] Rendering register page")
    return render_template('register.html')


@auth_bp.route("/check_session", methods=["GET"])
def check_session():
    if "user_id" in session:
        return jsonify({"logged_in": True, "username": session["username"]}), 200
    return jsonify({"logged_in": False}), 200
