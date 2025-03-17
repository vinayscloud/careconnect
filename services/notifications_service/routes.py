from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import mysql.connector
from db_config import get_db_connection
from auth_helper import token_required  # ✅ Using auth_service for token validation

notifications_bp = Blueprint("notifications", __name__)

@notifications_bp.route("/", methods=["GET"])
@token_required
def get_notifications(current_user):
    """Fetch notifications for doctors or patients based on user role."""
    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if current_user["role"] == "doctor":
            query = """
                SELECT id, patient_name AS name, appointment_date, appointment_time
                FROM appointments 
                WHERE doctor_id = %s AND appointment_date >= %s
                ORDER BY appointment_date ASC
            """
            cursor.execute(query, (current_user["id"], today))
        
        elif current_user["role"] == "patient":
            query = """
                SELECT id, doctor_name AS name, appointment_date, appointment_time
                FROM appointments 
                WHERE patient_id = %s AND appointment_date >= %s
                ORDER BY appointment_date ASC
            """
            cursor.execute(query, (current_user["id"], today))
        
        else:
            return jsonify({"error": "Unauthorized access"}), 403

        appointments = cursor.fetchall()
        cursor.close()
        conn.close()

        notifications = []
        
        for appointment in appointments:
            appointment_date = appointment["appointment_date"]
            appointment_time = appointment["appointment_time"]

            if appointment_date == today:
                display_date = "Today"
            elif appointment_date == tomorrow:
                display_date = "Tomorrow"
            else:
                display_date = appointment_date.strftime("%Y-%m-%d")

            if current_user["role"] == "doctor":
                message = f"You have an appointment with {appointment['name']} on {display_date} at {appointment_time}."
            else:
                message = f"Your appointment with {appointment['name']} is on {display_date} at {appointment_time}."

            notifications.append({
                "id": appointment["id"],
                "message": message,
                "display_date": display_date
            })

        return jsonify(notifications), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@notifications_bp.route("/read/<int:notification_id>", methods=["POST"])
@token_required
def mark_notification_as_read(current_user, notification_id):
    """Mark a notification as read so it doesn’t reappear."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "UPDATE appointments SET read_status = 1 WHERE id = %s"
        cursor.execute(query, (notification_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Notification marked as read."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
