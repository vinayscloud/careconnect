from flask import Blueprint, request, jsonify
from app.database import db
from app.models import Appointment

appointment_bp = Blueprint('appointments', __name__)

@appointment_bp.route('/book', methods=['POST'])
def book_appointment():
    try:
        data = request.get_json()

        appointment = Appointment(
            doctor_id=data['doctorId'],
            doctor_name=data['doctorName'],
            patient_name=data['name'],
            patient_email=data['email'],
            patient_phone=data['phone'],
            appointment_date=data['date'],
            appointment_time=data['time'],
            notes=data['notes']
        )

        db.session.add(appointment)
        db.session.commit()

        return jsonify({"message": "Appointment booked successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
