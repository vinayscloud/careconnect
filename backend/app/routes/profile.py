from flask import Blueprint, request, render_template, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.db_config import get_db_connection

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
def profile():
    user_id = request.args.get('user_id')  # Passed as query param

    if not user_id:
        return jsonify({'message': 'User ID is required', 'status': 'error'})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, email, role, user_status FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        return jsonify({'message': 'User not found', 'status': 'error'})

    return render_template('profile.html', user=user)

@profile_bp.route('/update_email', methods=['POST'])
def update_email():
    user_id = request.form.get('user_id')
    new_email = request.form.get('new_email')

    if not user_id or not new_email:
        return jsonify({'message': 'User ID and Email are required', 'status': 'error'})

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = %s WHERE id = %s", (new_email, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Email updated successfully', 'status': 'success'})

@profile_bp.route('/update_password', methods=['POST'])
def update_password():
    user_id = request.form.get('user_id')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')

    if not user_id or not old_password or not new_password:
        return jsonify({'message': 'All fields are required', 'status': 'error'})

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT password FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()

    if not user or not check_password_hash(user['password'], old_password):
        return jsonify({'message': 'Old password is incorrect', 'status': 'error'})

    # Hash new password and update in DB
    new_password_hash = generate_password_hash(new_password)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_password_hash, user_id))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Password updated successfully', 'status': 'success'})
