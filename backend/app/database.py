# This file contains the code to connect to the MySQL database. It uses the mysql-connector-python library to connect to the database. 
# The get_db_connection function returns a connection object that can be used to execute queries on the database.

# import mysql.connector
# from config import Config

# def get_db_connection():
#     return mysql.connector.connect(
#         host=Config.MYSQL_HOST,
#         user=Config.MYSQL_USER,
#         password=Config.MYSQL_PASSWORD,
#         database=Config.MYSQL_DB
#     )

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_db_connection():
    """Returns the active SQLAlchemy database session."""
    return db.session

