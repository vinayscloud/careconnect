from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()  # ✅ Ensures pymysql is used as MySQLdb

db = SQLAlchemy()

def init_db(app):
    """Initialize the database with Flask app context."""
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Create tables if they don’t exist
