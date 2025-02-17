from flask import Blueprint, request, jsonify
import mysql.connector
from flask_cors import CORS
from app.db_config import db_config, get_db_connection

admin_user_bp = Blueprint('admin_user', __name__)


@admin_user_bp.route('/search_user', methods=['GET'])
def search_user():
    """
    Search users by either:
    - Username or Email (using `username_or_email` query parameter)
    - User ID (using `user_id` query parameter)
    """
    username_or_email = request.args.get('username_or_email')
    user_id = request.args.get('user_id')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if user_id:  # Search by User ID
        sql = "SELECT id, username, email, role, user_status FROM users WHERE id = %s"
        cursor.execute(sql, (user_id,))
    elif username_or_email:  # Search by Username or Email
        sql = """
        SELECT id, username, email, role, user_status
        FROM users 
        WHERE username LIKE %s OR email LIKE %s
        """
        cursor.execute(sql, (f"%{username_or_email}%", f"%{username_or_email}%"))
    else:
        return jsonify([])  # Return empty list if no query

    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(users)


@admin_user_bp.route('/toggle_user_status', methods=['POST'])
def toggle_user_status():
    """
    Toggle a user's activation status.
    If the user is active, deactivate them (set `user_status = 'N'`).
    If the user is inactive, activate them (set `user_status = 'Y'`).
    """
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "Invalid user ID"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check the current status
    cursor.execute("SELECT user_status FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        return jsonify({"error": "User not found"}), 404

    current_status = user['user_status']
    new_status = 'N' if current_status != 'N' else 'Y'  # Toggle status

    # Update user status
    cursor.execute("UPDATE users SET user_status = %s WHERE id = %s", (new_status, user_id))
    conn.commit()

    cursor.close()
    conn.close()

    action = "Deactivated" if new_status == 'N' else "Activated"
    return jsonify({"message": f"User {action} successfully", "new_status": new_status})
