# This file contains the configuration for the Flask app. 
# It sets the MySQL database connection details and the secret key for the Flask app.

import os
from flask import Flask
from flask_cors import CORS


import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://admin:Clod123456789@database-1.cm1p8c8kitx3.us-east-1.rds.amazonaws.com/careconnect"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

 # ✅ Flask Session Configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "your_strong_secret_key")  # Use an environment variable for security
    SESSION_TYPE = "filesystem"  # Stores session data in server-side files
    SESSION_PERMANENT = False  # Session expires after inactivity
    SESSION_USE_SIGNER = True  # Prevents session tampering
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes (1800 seconds) of inactivity before auto logout
    SESSION_COOKIE_HTTPONLY = True  # Prevents JavaScript from accessing session cookies
    SESSION_COOKIE_SECURE = True  # Only send cookies over HTTPS (enable if HTTPS is used)
    SESSION_COOKIE_SAMESITE = "Lax"  # Prevents CSRF attacks while allowing safe cross-site navigation