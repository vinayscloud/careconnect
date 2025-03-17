import mysql.connector

db_config = {
    "host": "database-1.cm1p8c8kitx3.us-east-1.rds.amazonaws.com",
    "user": "admin",
    "password": "Clod123456789",
    "database": "careconnect"
}

def get_db_connection():
    """Establish and return a new database connection."""
    return mysql.connector.connect(**db_config)
