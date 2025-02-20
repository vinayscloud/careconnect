from flask import Blueprint, request, jsonify,render_template
import mysql.connector
from app.db_config import get_db_connection
from app.routes.auth import token_required
doctors_bp = Blueprint("doctors", __name__)

@doctors_bp.route('/get_doctors_portal', methods=['GET'])
@token_required
def get_doctors_portal(current_user):
    """ Renders the doctor portal page """
    if current_user["role"] != "patient":
        return jsonify({"error": "Unauthorized access"}), 403  # Prevent patients from accessing

    return render_template('doctor-profile.html', user=current_user)




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
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = "SELECT id, name, specialty, location, experience, rating FROM doctors WHERE 1=1"
        params = []

        if filters["search"]:
            query += " AND LOWER(name) LIKE %s"
            params.append(f"%{filters['search']}%")
        
        if filters["specialty"]:
            query += " AND LOWER(specialty) LIKE %s"
            params.append(f"%{filters['specialty']}%")
        
        if filters["city"]:
            query += " AND LOWER(location) LIKE %s"
            params.append(f"%{filters['city']}%")

        if filters["min_experience"]:
            query += " AND experience >= %s"
            params.append(int(filters["min_experience"]))

        if filters["min_rating"]:
            query += " AND rating >= %s"
            params.append(float(filters["min_rating"]))

        cursor.execute(query, tuple(params))
        doctors = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(doctors)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
