# This file contains the configuration for the Flask app. 
# It sets the MySQL database connection details and the secret key for the Flask app.

import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()



import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://admin:Clod123456789@database-1.cm1p8c8kitx3.us-east-1.rds.amazonaws.com/careconnect"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False



    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

    # ✅ Secure SMTP Configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")  # No hardcoded email
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")  # No hardcoded password
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", MAIL_USERNAME)  # Use the same email for sender
