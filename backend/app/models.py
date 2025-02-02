# This file contains the models for the application which are used to create the database tables. 
# The models are created using the SQLAlchemy ORM (Object-Relational Mapping) library. 
# The models define the structure of the database tables and the relationships between them.

# class Doctor:
#     def __init__(self, id, name, specialty, location, experience, rating):
#         self.id = id
#         self.name = name
#         self.specialty = specialty
#         self.location = location
#         self.experience = experience
#         self.rating = rating

# class Appointment:
#     def __init__(self, doctor_id, doctor_name, patient_name, email, phone, date, time, notes):
#         self.doctor_id = doctor_id
#         self.doctor_name = doctor_name
#         self.patient_name = patient_name
#         self.email = email
#         self.phone = phone
#         self.date = date
#         self.time = time
#         self.notes = notes

from app.database import db

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    doctor_name = db.Column(db.String(100), nullable=False)
    patient_name = db.Column(db.String(100), nullable=False)
    patient_email = db.Column(db.String(100), nullable=False)
    patient_phone = db.Column(db.String(20), nullable=False)
    appointment_date = db.Column(db.String(20), nullable=False)
    appointment_time = db.Column(db.String(20), nullable=False)
    notes = db.Column(db.Text)

