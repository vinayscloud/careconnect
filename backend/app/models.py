from app.database import db

class doctors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    experience = db.Column(db.Integer)
    rating = db.Column(db.Float)


class appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)  # Foreign Key linking to Doctor
    doctor_name = db.Column(db.String(100), nullable=False)  # Store the doctor's name for easy access
    patient_name = db.Column(db.String(255), nullable=False)  # Patient's full name
    patient_email = db.Column(db.String(255), nullable=False)  # Patient's email
    patient_phone = db.Column(db.String(20), nullable=False)  # Patient's phone number
    appointment_date = db.Column(db.Date, nullable=False)  # Date of the appointment
    appointment_time = db.Column(db.String(20), nullable=False)  # Time of the appointment
    notes = db.Column(db.Text)  # Notes regarding the appointment
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Timestamp for appointment creation