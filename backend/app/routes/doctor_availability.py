from flask import Blueprint, request, jsonify
from app.db_config import get_db_connection
from app.routes.auth import token_required
from datetime import time, timedelta

# Define Blueprint
doctor_availability_bp = Blueprint('doctor_availability_bp', __name__)

# ✅ 1. GET availability for a specific doctor and date
@doctor_availability_bp.route('/get', methods=['GET'])
@token_required
def get_availability(current_user):
    doctor_id = current_user['id']
    date = request.args.get('date')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT start_time, is_available, is_booked 
        FROM doctor_availability 
        WHERE doctor_id = %s AND availability_date = %s
    """, (doctor_id, date))

    data = cursor.fetchall()

    # ✅ Robustly format start_time
    for item in data:
        start = item.get("start_time")
        if isinstance(start, time):
            item["start_time"] = start.strftime("%H:%M")
        elif isinstance(start, timedelta):
            total_minutes = int(start.total_seconds() // 60)
            hours = total_minutes // 60
            minutes = total_minutes % 60
            item["start_time"] = f"{hours:02d}:{minutes:02d}"
        else:
            item["start_time"] = str(start)

    cursor.close()
    conn.close()
    return jsonify(data)


# ✅ 2. POST - Doctor updates availability
@doctor_availability_bp.route('/update_availability', methods=['POST'])
@token_required
def update_availability(current_user):
    if current_user['role'] != 'doctor':
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    date = data.get('date')
    availability = data.get('availability')  # List of {time, status}

    conn = get_db_connection()
    cursor = conn.cursor()

    for slot in availability:
        cursor.execute("""
            INSERT INTO doctor_availability (doctor_id, availability_date, start_time, is_available, is_booked)
            VALUES (%s, %s, %s, %s, 'N')
            ON DUPLICATE KEY UPDATE is_available = VALUES(is_available)
        """, (current_user['id'], date, slot['time'], slot['status']))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Availability updated successfully!"})


# ✅ 3. GET available slots (for patient side)
@doctor_availability_bp.route('/slots', methods=['GET'])
def get_slots_for_booking():
    doctor_id = request.args.get('doctor_id')
    date = request.args.get('date')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT start_time FROM doctor_availability 
        WHERE doctor_id = %s AND availability_date = %s AND is_available = 'Y' AND is_booked = 'N'
    """, (doctor_id, date))

    slots = cursor.fetchall()

    # ✅ Format time for frontend dropdown
    for item in slots:
        start = item.get("start_time")
        if isinstance(start, time):
            item["start_time"] = start.strftime("%H:%M")
        elif isinstance(start, timedelta):
            total_minutes = int(start.total_seconds() // 60)
            hours = total_minutes // 60
            minutes = total_minutes % 60
            item["start_time"] = f"{hours:02d}:{minutes:02d}"
        else:
            item["start_time"] = str(start)

    cursor.close()
    conn.close()
    return jsonify(slots)
