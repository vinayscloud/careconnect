from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
import mysql.connector
import hashlib
import datetime

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

# ✅ Login API (with Session Expiration & Role-Based Redirection)
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
            
            # ✅ Implement Session Expiration (30 minutes of inactivity)
            session['last_active'] = datetime.datetime.utcnow().timestamp()

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

# ✅ Logout API (Clears Session & Redirects)
@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    print("[DEBUG] Logging out user")
    session.clear()
    return jsonify({"message": "Logged out successfully!", "redirect": "/login"}), 200

# ✅ Session Expiration Check
@auth_bp.route("/check_session", methods=["GET"])
def check_session():
    user_id = session.get("user_id")

    if user_id:
        last_active = session.get("last_active", 0)
        current_time = datetime.datetime.utcnow().timestamp()
        
        # Check if session expired (30 minutes of inactivity)
        if current_time - last_active > 1800:  # 1800 seconds = 30 minutes
            print("[INFO] Session expired for user ID:", user_id)
            session.clear()
            return jsonify({"logged_in": False, "error": "Session expired"}), 401

        # Update last activity time
        session["last_active"] = current_time
        return jsonify({"logged_in": True, "username": session["username"]}), 200

    return jsonify({"logged_in": False}), 200

# ✅ Register API (RESTORED with Security Fixes)
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


# ✅ Fetch Patient Profile (Name & Email from Users, Other Fields from Patient_Profiles)
@auth_bp.route("/profile", methods=["GET"])
def get_profile():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    conn = create_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.username AS name, u.email, 
                   COALESCE(p.phone, '') AS phone, 
                   COALESCE(p.medical_history, '') AS medical_history, 
                   COALESCE(p.address, '') AS address
            FROM users u 
            LEFT JOIN patient_profiles p ON u.id = p.user_id 
            WHERE u.id = %s
        """, (session["user_id"],))
        
        profile = cursor.fetchone()
        if profile:
            return jsonify(profile), 200
        else:
            return jsonify({"error": "Profile not found"}), 404
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()


# ✅ Create Patient Profile
@auth_bp.route("/profile/create", methods=["POST"])
def create_profile():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    phone = data.get("phone")
    medical_history = data.get("medical_history")
    address = data.get("address")

    if not phone or not medical_history or not address:
        return jsonify({"error": "All fields are required"}), 400

    conn = create_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO patient_profiles (user_id, phone, medical_history, address) 
            VALUES (%s, %s, %s, %s)
        """, (session["user_id"], phone, medical_history, address))

        conn.commit()
        return jsonify({"message": "Profile created successfully!"}), 201
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

# ✅ Update Patient Profile (Edit)
@auth_bp.route("/profile/update", methods=["PUT"])
def update_profile():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    phone = data.get("phone")
    medical_history = data.get("medical_history")
    address = data.get("address")

    if not phone or not medical_history or not address:
        return jsonify({"error": "All fields are required"}), 400

    conn = create_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE patient_profiles 
            SET phone=%s, medical_history=%s, address=%s 
            WHERE user_id=%s
        """, (phone, medical_history, address, session["user_id"]))

        conn.commit()
        return jsonify({"message": "Profile updated successfully!"}), 200
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()

# ✅ Delete Patient Profile
@auth_bp.route("/profile/delete", methods=["DELETE"])
def delete_profile():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    conn = create_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patient_profiles WHERE user_id = %s", (session["user_id"],))

        conn.commit()
        return jsonify({"message": "Profile deleted successfully!"}), 200
    except mysql.connector.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    finally:
        cursor.close()
        conn.close()