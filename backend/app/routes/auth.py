# This file contains the routes for the application.

# This file contains the routes for the application.


from flask import Blueprint, jsonify, render_template, request
from app.database import get_db_connection  # Add this import statement
from app.database import db
from flask_cors import CORS

routes = Blueprint("routes", __name__)
CORS(routes)

# Fetch Doctors with Filters
@routes.route('/api/doctors', methods=['GET'])
def get_doctors():
    try:
        search_query = request.args.get('search', '').lower()
        specialty = request.args.get('specialty', '').lower()
        city = request.args.get('city', '').lower()
        min_experience = request.args.get('min_experience', '')
        min_rating = request.args.get('min_rating', '')

        query = "SELECT * FROM doctors WHERE 1=1"
        params = []

        if search_query:
            query += " AND LOWER(name) LIKE :search"
            params.append({"search": f"%{search_query}%"})

        if specialty:
            query += " AND LOWER(specialty) LIKE :specialty"
            params.append({"specialty": f"%{specialty}%"})

        if city:
            query += " AND LOWER(location) LIKE :city"
            params.append({"city": f"%{city}%"})

        if min_experience.isdigit():
            query += " AND experience >= :min_experience"
            params.append({"min_experience": int(min_experience)})

        if min_rating.isdigit():
            query += " AND rating >= :min_rating"
            params.append({"min_rating": float(min_rating)})

        result = db.session.execute(query, params)
        doctors = [dict(row) for row in result]

        return jsonify(doctors)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve the Doctor Profile Page
@routes.route('/')
def index():
    return render_template("doctor-profile.html")

# Booking Form Route
@routes.route('/booking-form', methods=['GET'])
def booking_form():
    doctor_id = request.args.get('doctorId')

    try:
        doctor = db.session.execute(
            "SELECT * FROM doctors WHERE id = :id", {"id": doctor_id}
        ).fetchone()

        if doctor:
            return render_template('booking-form.html', doctor=dict(doctor))
        else:
            return jsonify({"error": "Doctor not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API Endpoint for Booking Appointment
@routes.route('/api/book-appointment', methods=['POST'])
def book_appointment():
    try:
        data = request.get_json()

        doctor_id = data.get('doctorId')
        doctor_name = data.get('doctorName')
        patient_name = data.get('name')
        patient_email = data.get('email')
        patient_phone = data.get('phone')
        appointment_date = data.get('date')
        appointment_time = data.get('time')
        notes = data.get('notes')

        conn = get_db_connection()
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO appointments (doctor_id, doctor_name, patient_name, patient_email, patient_phone, 
                                      appointment_date, appointment_time, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (doctor_id, doctor_name, patient_name, patient_email, patient_phone, 
                                      appointment_date, appointment_time, notes))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Appointment booked successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
