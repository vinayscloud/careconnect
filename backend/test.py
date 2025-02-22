import mysql.connector
from datetime import datetime

# ✅ Update with your actual database credentials
db_config = {
    "host": "database-1.cm1p8c8kitx3.us-east-1.rds.amazonaws.com",
    "user": "admin",
    "password": "Clod123456789",
    "database": "careconnect"
}

# ✅ Connect to the database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor(dictionary=True)

today = datetime.today().date()

# ✅ Replace with an actual doctor ID from your database
doctor_id = 48  # Change this to the doctor ID you're testing

query = """
    SELECT patient_name AS name, appointment_date
    FROM appointments 
    WHERE doctor_id = %s AND appointment_date >= %s
    ORDER BY appointment_date ASC
"""
cursor.execute(query, (doctor_id, today))
appointments = cursor.fetchall()

# ✅ Print fetched appointments
print("🔍 TEST OUTPUT: ", appointments)

cursor.close()
conn.close()
