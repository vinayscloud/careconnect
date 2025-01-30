from flask import Flask, jsonify, render_template, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MySQL Database Configuration (Hardcoded)
db_config = {
    "host": "database-1.cm1p8c8kitx3.us-east-1.rds.amazonaws.com",
    "user": "admin",
    "password": "Clod123456789",
    "database": "careconnect"
}

# API Endpoint to Fetch Doctors with Filters
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Get filter parameters from request
        search_query = request.args.get('search', '').lower()  # Search by name
        specialty = request.args.get('specialty', '').lower()
        city = request.args.get('city', '').lower()
        min_experience = request.args.get('min_experience', '')
        min_rating = request.args.get('min_rating', '')

        # Base SQL Query
        query = "SELECT * FROM doctors WHERE 1=1"
        params = []

        # Apply filters dynamically
        if search_query:
            query += " AND LOWER(name) LIKE %s"
            params.append(f"%{search_query}%")

        if specialty:
            query += " AND LOWER(specialty) LIKE %s"
            params.append(f"%{specialty}%")

        if city:
            query += " AND LOWER(location) LIKE %s"
            params.append(f"%{city}%")

        if min_experience.isdigit():
            query += " AND experience >= %s"
            params.append(int(min_experience))

        if min_rating.isdigit():
            query += " AND rating >= %s"
            params.append(float(min_rating))

        # Execute query
        cursor.execute(query, params)
        doctors = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(doctors)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve the Doctor Profile Page
@app.route('/')
def index():
    return render_template("doctor-profile.html")

# Route to Show Booking Form with Doctor Information
@app.route('/booking-form', methods=['GET'])
def booking_form():
    doctor_id = request.args.get('doctorId')
    
    # Fetch the doctor details from the database to pre-fill the form
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM doctors WHERE id = %s", (doctor_id,))
        doctor = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if doctor:
            return render_template('booking-form.html', doctor=doctor)
        else:
            return jsonify({"error": "Doctor not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API Endpoint for Booking Appointment
@app.route('/api/book-appointment', methods=['POST'])
def book_appointment():
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

        return jsonify({"message": "Appointment booked successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
