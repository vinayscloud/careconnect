
# This file is the entry point for the Flask application. 
# It creates the Flask app instance and registers the routes blueprint. 
# The create_app function initializes the Flask app, sets the configuration, and registers the routes blueprint. 
# The app.run() method starts the Flask development server.    

# import os
# from flask import Flask
# from flask_cors import CORS
# from app.config import Config
# from app.database import db

# # Import Blueprints
# from app.routes.doctors import doctor_bp
# from app.routes.appointments import appointment_bp
# from app.routes.auth import main  # Assuming this blueprint is used for auth routes

# def create_app():
#     # Get the absolute path of the frontend folder
#     frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/pages"))

#     # Initialize Flask with custom template folder
#     app = Flask(__name__, template_folder=frontend_path)

#     app.config.from_object(Config)
#     CORS(app)  # Enable CORS for frontend

#     # Initialize database with app
#     db.init_app(app)

#     # Register Blueprints with proper prefixes if needed
#     app.register_blueprint(doctor_bp, url_prefix='/api/doctors')
#     app.register_blueprint(appointment_bp, url_prefix='/api/appointments')
#     app.register_blueprint(main)  # Assuming this one handles routes like '/'

#     return app


import os
from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.database import db

def create_app():
    # Initialize Flask App
    app = Flask(__name__)
    
    # Get the absolute path of the frontend folder
    # frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/pages"))

    # Set Configurations
    app.config.from_object(Config)
    CORS(app)  # Enable CORS for frontend

    # Initialize Database
    db.init_app(app)

    # Register Blueprints
    from app.routes.doctors import doctor_bp
    from app.routes.appointments import appointment_bp
    from app.routes.auth import routes  # Corrected from `main` to `routes`

    app.register_blueprint(doctor_bp, url_prefix='/api/doctors')
    app.register_blueprint(appointment_bp, url_prefix='/api/appointments')
    app.register_blueprint(routes)  # Register the `routes` Blueprint

    return app
