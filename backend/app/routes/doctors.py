from flask import Blueprint, request, jsonify
from app.services.doctor_service import DoctorService

doctors_bp = Blueprint("doctors", __name__)

@doctors_bp.route("/", methods=["GET"])
def get_doctors():
    filters = {
        "search": request.args.get("search", "").lower(),
        "specialty": request.args.get("specialty", "").lower(),
        "city": request.args.get("city", "").lower(),
        "min_experience": request.args.get("min_experience", ""),
        "min_rating": request.args.get("min_rating", ""),
    }
    
    try:
        doctors = DoctorService.get_doctors(filters)
        return jsonify(doctors)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
