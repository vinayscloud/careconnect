## Login Page Credentials
User: test@example.com
Password: password123

## Use this to run fronend side of the project on your local system
Name: Live Server
https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer

---

## Ensure Dependencies Are Installed**
Make sure you have installed the required packages:
```sh
pip install flask flask-sqlalchemy flask-cors pymysql mysql-connector-python
```



# CareConnect - Healthcare Appointment System

CareConnect is a web-based healthcare application that helps patients connect with family doctors in Canada. It allows users to search for doctors, book appointments, and manage their healthcare needs efficiently.

## 🚀 Features
- Search for doctors based on name, specialty, location, experience, and rating.
- Book appointments with doctors.
- Secure API endpoints with Flask.
- Cloud-native infrastructure using AWS & Azure.

---

## 🛠 Installation & Setup

### **1. Clone the Repository**
```sh
git clone https://github.com/your-username/CareConnect.git
cd CareConnect/backend
```

### **2. Set Up Virtual Environment (Optional but Recommended)**
```sh
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate  # For Windows
```

### **3. Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4. Configure the Database**
Update the `config.py` file with your database credentials:
```python
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:your_password@your_rds_endpoint/careconnect"
```

### **5. Run Migrations (If using Flask-Migrate)**
```sh
flask db upgrade
```

### **6. Run the Application**
```sh
python run.py
```
Application will start at **`http://127.0.0.1:5000/`**.

---

## 🛠 Troubleshooting

### **1. ModuleNotFoundError: No module named 'MySQLdb'**
Run:
```sh
pip install pymysql
```
And update `config.py`:
```python
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:your_password@your_rds_endpoint/careconnect"
```

### **2. Error: Flask-SQLAlchemy KeyError**
Ensure `flask_sqlalchemy` is installed:
```sh
pip install flask-sqlalchemy
```