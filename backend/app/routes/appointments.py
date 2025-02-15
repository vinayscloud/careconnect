from flask import Blueprint, request, jsonify, render_template
import mysql.connector
from flask_cors import CORS
from app.routes.auth import token_required

# MySQL Database Configuration (Hardcoded)
db_config = {
    "host": "database-1.cm1p8c8kitx3.us-east-1.rds.amazonaws.com",
    "user": "admin",
    "password": "Clod123456789",
    "database": "careconnect"
}

appointments_bp = Blueprint('appointments', __name__)

# Route to handle both GET and POST methods

@appointments_bp.route('/booking-form', methods=['GET', 'POST'])
@token_required
def booking_form():
    if request.method == 'GET':
        doctor_id = request.args.get('doctorId')  # Retrieve doctorId from URL parameters

        if not doctor_id:
            return jsonify({"error": "Doctor ID is required"}), 400  # Handle missing doctor ID

        # Directly using mysql.connector.connect for database connection
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM doctors WHERE id = %s", (doctor_id,))
            doctor = cursor.fetchone()
            cursor.close()
            conn.close()

            if doctor:
                return render_template('booking-form.html', doctor=doctor)  # Pass doctor details to template
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
            doctor_name = data.get('doctorName')
            patient_name = data.get('name')
            patient_email = data.get('email')
            patient_phone = data.get('phone')
            appointment_date = data.get('date')
            appointment_time = data.get('time')
            notes = data.get('notes')

            # Insert appointment details into the database
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Insert query for appointments table
            insert_query = """
                INSERT INTO appointments (doctor_id, doctor_name, patient_name, patient_email, patient_phone, 
                                          appointment_date, appointment_time, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (doctor_id, doctor_name, patient_name, patient_email, patient_phone, 
                                          appointment_date, appointment_time, notes))

            # Commit the transaction and close the connection
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"success": True, "message": "Appointment booked successfully!"}), 200
        except mysql.connector.Error as err:
            return jsonify({"success": False, "error": str(err)}), 500
