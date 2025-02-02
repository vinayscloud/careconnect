from flask import Blueprint, request, jsonify, render_template
from app.database import db
from app.models import Doctor

doctor_bp = Blueprint('doctors', __name__)

@doctor_bp.route('/', methods=['GET'])
def home():
    return render_template("../../pages/doctor-profile.html")  # This will now load from frontend/pages/

def get_doctors():

    try:
        search_query = request.args.get('search', '').lower()
        specialty = request.args.get('specialty', '').lower()
        city = request.args.get('city', '').lower()
        min_experience = request.args.get('min_experience', '')
        min_rating = request.args.get('min_rating', '')

        query = Doctor.query

        if search_query:
            query = query.filter(Doctor.name.ilike(f"%{search_query}%"))

        if specialty:
            query = query.filter(Doctor.specialty.ilike(f"%{specialty}%"))

        if city:
            query = query.filter(Doctor.location.ilike(f"%{city}%"))

        if min_experience.isdigit():
            query = query.filter(Doctor.experience >= int(min_experience))

        if min_rating.isdigit():
            query = query.filter(Doctor.rating >= float(min_rating))

        doctors = query.all()

        return jsonify([{
            "id": doc.id,
            "name": doc.name,
            "specialty": doc.specialty,
            "location": doc.location,
            "experience": doc.experience,
            "rating": doc.rating
        } for doc in doctors])

    except Exception as e:
        return jsonify({"error": str(e)}), 500
