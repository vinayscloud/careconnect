# This file contains the configuration for the Flask app. 
# It sets the MySQL database connection details and the secret key for the Flask app.

import os
from flask import Flask
from flask_cors import CORS

# class Config:
#     MYSQL_HOST = "database-1.cm1p8c8kitx3.us-east-1.rds.amazonaws.com"
#     MYSQL_USER = "admin"
#     MYSQL_PASSWORD = "Clod123456789"
#     MYSQL_DB = "careconnect"
#     SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")


import os

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:Clod123456789@database-1.cm1p8c8kitx3.us-east-1.rds.amazonaws.com/careconnect"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key_here")



