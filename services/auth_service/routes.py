from flask import Blueprint, request, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import os
from db_config import get_db_connection

auth_bp = Blueprint('auth', __name__)

SECRET_KEY = os.getenv("SECRET_KEY", "d28ab6f8995286e60aed281a574c18a03ff99490de1ab1f6")


@auth_bp.route("/signup", methods=["POST"])
def signup():
    """Handle user registration."""
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not username or not email or not password or not role:
        return jsonify({"error": "All fields are required!"}), 400

    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        return jsonify({"error": "User already exists!"}), 400

    # Insert new user
    cursor.execute(
        "INSERT INTO users (username, email, password, role, user_status) VALUES (%s, %s, %s, %s, %s)",
        (username, email, hashed_password, role, "active"),
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "User created successfully!"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login and return JWT token."""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user or not check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    if user['user_status'] == 'N':
        return jsonify({"error": "Your account is deactivated."}), 403

    # Generate JWT token
    token = jwt.encode(
        {'user_id': user['id'], 'exp': datetime.utcnow() + timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({"token": token, "message": "Login successful!"})

blacklisted_tokens = set()

@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Logout by blacklisting JWT token in memory."""
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"error": "Token is required"}), 400

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        blacklisted_tokens.add(token)

        return jsonify({"message": "Successfully logged out!"}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has already expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

@auth_bp.route("/validate_token", methods=["POST"])
def validate_token():
    """Validate JWT token and check blacklist."""
    data = request.get_json()
    token = data.get("token")

    if not token:
        return jsonify({"error": "Token is required"}), 400

    try:
        if token in blacklisted_tokens:
            return jsonify({"error": "Token is blacklisted. Please log in again."}), 401

        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded_token["user_id"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, email, role FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify(user)

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
