from flask import Blueprint, request, session, jsonify
from werkzeug.security import generate_password_hash
from app.db_config import get_db_connection

doctor_update_bp = Blueprint('doctor_update_bp', __name__)

# ✅ GET doctor profile
@doctor_update_bp.route('/api/doctor/update-profile', methods=['GET'])
def fetch_profile_data():
    if 'token' not in session or 'email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    email = session.get('email')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM doctors_profile WHERE email = %s", (email,))
    profile = cursor.fetchone()
    cursor.close()
    conn.close()

    if not profile:
        return jsonify({'error': 'Doctor profile not found'}), 404

    # ✅ Check if profile is complete
    required_fields = ['full_name', 'specialty', 'phone', 'address', 'experience', 'bio']
    is_complete = all(profile.get(field) for field in required_fields)

    profile['password'] = '*******'
    profile['is_complete'] = is_complete
    profile['user_status'] = profile.get('user_status', 'active')
    return jsonify(profile)

# ✅ POST: update profile fields + user_status
@doctor_update_bp.route('/api/doctor/update-profile', methods=['POST'])
def update_profile():
    print("🔧 Updating doctor profile...")
    if 'token' not in session or 'email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    email = session['email']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE doctors_profile
        SET full_name=%s, specialty=%s, phone=%s,
            address=%s, experience=%s, bio=%s, user_status=%s
        WHERE email=%s
    """, (
        data.get("full_name"), data.get("specialty"), data.get("phone"),
        data.get("address"), data.get("experience"), data.get("bio"),
        data.get("user_status"), email
    ))

    # ✅ Sync status with users table
    cursor.execute("UPDATE users SET user_status=%s WHERE email=%s", (data.get("user_status"), email))

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Profile updated successfully.")
    return jsonify({'message': 'Profile updated successfully'})

# ✅ POST: update password only
@doctor_update_bp.route('/api/doctor/update-password', methods=['POST'])
def update_password():
    print("🔒 Updating password...")
    if 'token' not in session or 'email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    new_pw = data.get("new_password")
    confirm_pw = data.get("confirm_password")

    if not new_pw or not confirm_pw:
        return jsonify({'error': 'Password fields are required'}), 400

    if new_pw != confirm_pw:
        return jsonify({'error': 'Passwords do not match'}), 400

    hashed = generate_password_hash(new_pw)
    email = session['email']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE doctors_profile SET password=%s WHERE email=%s", (hashed, email))
    cursor.execute("UPDATE users SET password=%s WHERE email=%s", (hashed, email))
    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Password updated in both tables.")
    return jsonify({'message': 'Password updated successfully'})
