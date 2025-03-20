from flask import Blueprint, request, jsonify
from app.db_config import get_db_connection
from app.routes.auth import token_required

doctor_patient_records_bp = Blueprint('doctor_patient_records', __name__)

# **1️⃣ Fetch Records for a Doctor (Only Their Patients)**
@doctor_patient_records_bp.route('/doctor/records', methods=['GET'])
@token_required
def get_doctor_records(current_user):
    if current_user['role'] != 'doctor':
        return jsonify({"error": "Unauthorized access"}), 403

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT pdr.record_id, pdr.appointment_id, u.username AS patient_name, 
               a.appointment_date, a.appointment_time, pdr.doctor_notes, pdr.patient_notes
        FROM patient_doctor_records pdr
        JOIN appointments a ON pdr.appointment_id = a.id
        JOIN users u ON pdr.patient_id = u.id
        WHERE pdr.doctor_id = %s
    """, (current_user['id'],))

    records = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(records)

# **2️⃣ Fetch Records for a Patient (Only Their Appointments)**
@doctor_patient_records_bp.route('/patient/records', methods=['GET'])
@token_required
def get_patient_records(current_user):
    if current_user['role'] != 'patient':
        return jsonify({"error": "Unauthorized access"}), 403

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT pdr.record_id, pdr.appointment_id, u.username AS doctor_name, 
               a.appointment_date, a.appointment_time, pdr.doctor_notes, pdr.patient_notes
        FROM patient_doctor_records pdr
        JOIN appointments a ON pdr.appointment_id = a.id
        JOIN users u ON pdr.doctor_id = u.id
        WHERE pdr.patient_id = %s
    """, (current_user['id'],))

    records = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(records)

# **3️⃣ Doctor Updates Medical Notes**
@doctor_patient_records_bp.route('/doctor/records/<int:record_id>', methods=['PUT'])
@token_required
def update_doctor_notes(current_user, record_id):
    if current_user['role'] != 'doctor':
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.json
    doctor_notes = data.get('doctor_notes')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE patient_doctor_records 
        SET doctor_notes = %s 
        WHERE record_id = %s AND doctor_id = %s
    """, (doctor_notes, record_id, current_user['id']))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Doctor's notes updated successfully!"})

# **4️⃣ Patient Updates Their Own Notes**
@doctor_patient_records_bp.route('/patient/records/<int:record_id>', methods=['PUT'])
@token_required
def update_patient_notes(current_user, record_id):
    if current_user['role'] != 'patient':
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.json
    patient_notes = data.get('patient_notes')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE patient_doctor_records 
        SET patient_notes = %s 
        WHERE record_id = %s AND patient_id = %s
    """, (patient_notes, record_id, current_user['id']))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Your notes updated successfully!"})
