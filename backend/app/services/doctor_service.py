from app.models import doctors, db

class DoctorService:
    @staticmethod
    def get_doctors(filters):
        query = doctors.query

        if filters.get("search"):
            query = query.filter(doctors.name.ilike(f"%{filters['search']}%"))
        
        if filters.get("specialty"):
            query = query.filter(doctors.specialty.ilike(f"%{filters['specialty']}%"))
        
        if filters.get("city"):
            query = query.filter(doctors.location.ilike(f"%{filters['city']}%"))

        if filters.get("min_experience"):
            query = query.filter(doctors.experience >= int(filters["min_experience"]))

        if filters.get("min_rating"):
            query = query.filter(doctors.rating >= float(filters["min_rating"]))

        return [{"id": d.id, "name": d.name, "specialty": d.specialty, "location": d.location,
                 "experience": d.experience, "rating": d.rating} for d in query.all()]
