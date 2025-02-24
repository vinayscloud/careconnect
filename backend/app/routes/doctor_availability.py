from flask import Blueprint, request, jsonify, render_template
import mysql.connector
from datetime import datetime, timedelta
from app.db_config import get_db_connection
from app.routes.auth import token_required

doctor_availability_bp = Blueprint('doctor_availability', __name__)

@doctor_availability_bp.route('/get_availability', methods=['GET'])
@token_required
def get_availability(current_user):
    """Fetches the availability of the doctor for the selected date."""
    if current_user["role"] != "doctor":
        return jsonify({"error": "Unauthorized access"}), 403

    doctor_id = current_user["id"]
    date = request.args.get('date')

    if not date:
        return jsonify({"error": "Date is required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('''
            SELECT TIME_FORMAT(start_time, '%H:%i') AS start_time, 
                   TIME_FORMAT(end_time, '%H:%i') AS end_time,
                   status, 
                   booked
            FROM doctor_availability
            WHERE id = %s AND availability_date = %s
        ''', (doctor_id, date))
        
        availability_slots = cursor.fetchall()
        cursor.close()
        conn.close()

        if not availability_slots:
            return jsonify([])

        return jsonify(availability_slots)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@doctor_availability_bp.route('/update_availability', methods=['POST'])
@token_required
def update_availability(current_user):
    """Updates the availability of the doctor."""
    if current_user["role"] != "doctor":
        return jsonify({"error": "Unauthorized access"}), 403

    doctor_id = current_user["id"]
    data = request.json
    date = data.get('date')
    availability = data.get('availability')

    if not date or not availability:
        return jsonify({"error": "Date and availability data are required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        for slot in availability:
            time = slot['time']
            status = slot['status']
            start_time = datetime.strptime(time, '%H:%M').strftime('%H:%M:00')
            end_time = (datetime.strptime(start_time, '%H:%M:%S') + timedelta(minutes=30)).strftime('%H:%M:00')

            if status == 'NOT AVAILABLE':
                # Update the slot to set status and booked = 'NO'
                cursor.execute('''
                    UPDATE doctor_availability
                    SET status = 'NOT AVAILABLE', booked = 'NO'
                    WHERE id = %s AND availability_date = %s AND start_time = %s AND end_time = %s
                ''', (doctor_id, date, start_time, end_time))
            elif status == 'AVAILABLE':
                # Update the slot to set status to AVAILABLE without affecting booked
                cursor.execute('''
                    UPDATE doctor_availability
                    SET status = 'AVAILABLE'
                    WHERE id = %s AND availability_date = %s AND start_time = %s AND end_time = %s
                ''', (doctor_id, date, start_time, end_time))

            # Insert the slot if it doesn't exist
            cursor.execute('''
                INSERT INTO doctor_availability (id, availability_date, start_time, end_time, booked, status)
                SELECT %s, %s, %s, %s, 'NO', %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM doctor_availability
                    WHERE id = %s AND availability_date = %s AND start_time = %s AND end_time = %s
                )
            ''', (doctor_id, date, start_time, end_time, status, doctor_id, date, start_time, end_time))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Availability updated successfully."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@doctor_availability_bp.route('/doctor-availability')
@token_required
def doctor_availability_page(current_user):
    """Render the doctor availability page."""
    if current_user["role"] != "doctor":
        return jsonify({"error": "Unauthorized access"}), 403

    return render_template('doctor-availability.html')