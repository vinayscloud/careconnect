from flask import Blueprint, request, jsonify, render_template
from app.db_config import db_config , get_db_connection
from app.routes.auth import token_required
doctor_view_appointments_bp = Blueprint('doctor_portal', __name__)

@doctor_view_appointments_bp.route('/view_doctor_portal', methods=['GET'])
@token_required
def doctor_portal(current_user):
    """ Renders the doctor portal page """
    if current_user["role"] != "doctor":
        return jsonify({"error": "Unauthorized access"}), 403  # Prevent patients from accessing

    return render_template('view_doctor_appointments.html', doctor_id=current_user["id"])


@doctor_view_appointments_bp.route('/view_doctor_appointments', methods=['GET'])
@token_required
def doctor_appointments(current_user):
    """ Fetches all appointments for the logged-in doctor """
    if current_user["role"] != "doctor":
        return jsonify({"error": "Unauthorized access"}), 403

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT id, patient_name, patient_email, patient_phone, appointment_date, 
               appointment_time, notes 
        FROM appointments WHERE doctor_id = %s ORDER BY appointment_date, appointment_time
        """
        cursor.execute(query, (current_user["id"],))
        appointments = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({"success": True, "appointments": appointments}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
