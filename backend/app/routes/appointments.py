from flask import Blueprint, request, jsonify, render_template
import mysql.connector
from flask_cors import CORS
from app.db_config import db_config , get_db_connection
from app.routes.auth import token_required

appointments_bp = Blueprint('appointments', __name__)

# Route to handle both GET and POST methods
@appointments_bp.route('/booking-form', methods=['GET', 'POST'])
@token_required
def booking_form(current_user):
    if request.method == 'GET':
        doctor_id = request.args.get('doctorId')  # Retrieve doctorId from URL parameters

        if not doctor_id:
            return jsonify({"error": "Doctor ID is required"}), 400  # Handle missing doctor ID

        # Directly using mysql.connector.connect for database connection
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM doctors WHERE id = %s", (doctor_id,))
            doctor = cursor.fetchone()
            cursor.close()
            conn.close()

            if doctor:
                return render_template('booking-form.html', doctor=doctor, patient_id=current_user['id'])  # Pass doctor details & patient_id
            else:
                return jsonify({"error": "Doctor not found"}), 404  # Handle invalid doctor ID

        except mysql.connector.Error as err:
            return jsonify({"error": f"Database error: {str(err)}"}), 500

    elif request.method == 'POST':
        # Handle POST request for booking appointment
        try:
            # Get appointment data from request
            data = request.get_json()

            # Extract doctor and patient details from the form data
            doctor_id = data.get('doctorId')
            patient_id = data.get('patientId')  # Now patient_id comes from frontend
            doctor_name = data.get('doctorName')
            patient_name = data.get('name')
            patient_email = data.get('email')
            patient_phone = data.get('phone')
            appointment_date = data.get('date')
            appointment_time = data.get('time')
            notes = data.get('notes')

            if not all([doctor_id, patient_id, doctor_name, patient_name, patient_email, appointment_date, appointment_time]):
                return jsonify({"error": "Missing required fields"}), 400

            # Insert appointment details into the database
            conn = get_db_connection()
            cursor = conn.cursor()

            insert_query = """
                INSERT INTO appointments (patient_id, doctor_id, doctor_name, patient_name, patient_email, patient_phone, 
                                          appointment_date, appointment_time, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (patient_id, doctor_id, doctor_name, patient_name, patient_email, patient_phone, 
                                          appointment_date, appointment_time, notes))

            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"success": True, "message": "Appointment booked successfully!"}), 200
        except mysql.connector.Error as err:
            return jsonify({"success": False, "error": str(err)}), 500