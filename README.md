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



---

### **1. `.github` Folder**
- This folder is typically used for GitHub-related configurations like workflows for **CI/CD pipelines**.
- It may contain YAML files defining GitHub Actions for automating builds, tests, and deployments.

---

### **2. `backend` Folder**
This folder contains the backend logic of the application. Within it:

#### **`app` Subfolder**
This is the main backend application, structured into submodules:

##### **a. `routes/`**
- Contains Python files for defining API endpoints:
  - `appointments.py` - Handles appointment-related endpoints.
  - `auth.py` - Manages authentication (e.g., login, registration).
  - `doctors.py` - Manages doctor-related endpoints.

##### **b. `services/`**
- Implements business logic for different features:
  - `appointment_service.py` - Handles appointment-related operations.
  - `auth_service.py` - Deals with authentication logic (e.g., token generation, user validation).
  - `doctor_service.py` - Handles doctor-related services.
  - `config.py` - Likely contains environment configurations (e.g., database credentials, API keys).
  - `database.py` - Handles database connections and ORM models.
  - `models.py` - Defines database models (tables and relationships).

##### **c. Other Files**
- `tests/` - Likely contains unit and integration tests.
- `venv/` - Virtual environment folder for Python dependencies.
- `run.py` - The main entry point for running the backend server.

---

### **3. `docker` Folder**
- Likely contains **Docker-related files** such as:
  - `Dockerfile` (for building backend container)
  - `docker-compose.yml` (for orchestrating multiple services like database and backend).

---

### **4. `frontend` Folder**
This folder contains the frontend application, possibly built with React, Vue, or Angular.

#### **Subfolders:**
- `assets/` - Stores static assets like:
  - `images/` - Contains images used in the frontend.
  - `scripts/` - Might include helper scripts for frontend logic.
  - `styles/` - Likely contains CSS/SCSS files for styling.
- `pages/` - Likely contains frontend page components.

---

### **5. `infrastructure` Folder**
This folder manages cloud infrastructure, likely using **Terraform** (as suggested by `.tf` files).

#### **Modules Subfolder**
- `ec2/` - Configuration for deploying EC2 instances.
- `iam/` - IAM role definitions (user permissions).
- `s3/` - Configurations for S3 storage.
- `vpc/` - Network setup (VPC, subnets, etc.).

---

### **6. Infrastructure Files**
- `.terraform.lock.hcl` - Lock file to ensure Terraform uses the correct provider versions.
- `main.tf` - Main Terraform configuration.
- `providers.tf` - Defines cloud provider details (e.g., AWS, Azure).
- `terraform.tfstate` & `terraform.tfvars` - Stores Terraform state and variables.
- `variables.tf` - Defines Terraform variables.

---

### **7. Miscellaneous Files**
- `.gitignore` - Specifies files and folders to ignore in Git version control.
- `README.md` - Documentation for setting up and running the project.
- `requirements.txt` - Lists Python dependencies for the backend.

---

### **Summary**
This project follows a **well-structured** full-stack architecture:
1. **Backend** (Python, FastAPI or Flask, using services and routes).
2. **Frontend** (React, Vue, or Angular with assets and pages).
3. **Infrastructure** (Terraform for cloud deployment).
4. **Docker** support for containerization.

This setup is **modular, scalable, and cloud-friendly**, making it ideal for a production-ready application. 🚀
