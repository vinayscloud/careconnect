from flask import Blueprint, request, jsonify, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

profile_bp = Blueprint('profile', __name__)

# Database Configuration
DB_CONFIG = {
    "host": "database-1.cm1p8c8kitx3.us-east-1.rds.amazonaws.com",
    "user": "admin",
    "password": "Clod123456789",
    "database": "careconnect"
}

# Function to establish a database connection
def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


@profile_bp.route('/profile', methods=['GET'])
def get_profile():
    """Fetch user profile details and autofill existing information."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch user details from `users` table
        cursor.execute("SELECT username, email, password FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        # Fetch additional patient profile details (excluding medical history)
        cursor.execute("SELECT full_name, phone FROM patient_profiles WHERE user_id = %s", (user_id,))
        profile = cursor.fetchone()

        if user and profile:
            response = {
                "full_name": profile["full_name"],  # Full Name should not be editable
                "email": user["email"],
                "phone": profile["phone"],
                "current_password": user["password"]
            }
            return jsonify(response), 200
        else:
            return jsonify({'error': 'Profile not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@profile_bp.route('/profile/update', methods=['POST'])
def update_profile():
    """Allow users to edit only Email and Phone."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    phone = data.get('phone')
    email = data.get('email')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Update `users` table (email)
        cursor.execute("UPDATE users SET email = %s WHERE id = %s", (email, user_id))

        # Update `patient_profiles` table (phone only)
        cursor.execute("UPDATE patient_profiles SET phone = %s WHERE user_id = %s", (phone, user_id))

        conn.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@profile_bp.route('/profile/change-password', methods=['POST'])
def change_password():
    """Allow password change only if the new password is different from the current one."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.json
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch the current password
        cursor.execute("SELECT password FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        if not user or not check_password_hash(user['password'], old_password):
            return jsonify({'error': 'Incorrect old password'}), 400

        if check_password_hash(user['password'], new_password):
            return jsonify({'error': 'New password cannot be the same as the current password'}), 400

        # Hash new password
        hashed_password = generate_password_hash(new_password)

        # Update password
        cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_password, user_id))
        conn.commit()

        return jsonify({'message': 'Password updated successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
