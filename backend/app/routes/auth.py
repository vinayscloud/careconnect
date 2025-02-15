from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps

# Create a Blueprint for the 'auth' module
auth_bp = Blueprint('auth', __name__)

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        user='admin',
        host='database-1.cm1p8c8kitx3.us-east-1.rds.amazonaws.com',
        password='Clod123456789',
        database='careconnect'
    )

# JWT Token Verification Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get('token')
        if not token:
            return redirect(url_for('auth.login_page'))
        try:
            data = jwt.decode(token, 'd28ab6f8995286e60aed281a574c18a03ff99490de1ab1f6', algorithms=["HS256"])
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE id = %s", (data['user_id'],))
            current_user = cursor.fetchone()
            cursor.close()
            conn.close()
            if not current_user:
                return redirect(url_for('auth.login_page'))
        except jwt.ExpiredSignatureError:
            return redirect(url_for('auth.login_page'))
        except jwt.InvalidTokenError:
            return redirect(url_for('auth.login_page'))

        return f(current_user, *args, **kwargs)
    return decorated






@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            return render_template('login.html', error="Invalid credentials")

        # Check if the user is deactivated
        if user['user_status'] == 'N':
            return render_template('login.html', error="Your account is deactivated.")

        # Verify password
        if not check_password_hash(user['password'], password):
            return render_template('login.html', error="Invalid credentials")

        # Generate JWT Token
        token = jwt.encode(
            {'user_id': user['id'], 'exp': datetime.utcnow() + timedelta(hours=1)},
            'd28ab6f8995286e60aed281a574c18a03ff99490de1ab1f6',
            algorithm="HS256"
        )

        session['token'] = token  # Store JWT in session
        return redirect(url_for('auth.dashboard'))

    return render_template('login.html')


# Signup Page
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        if request.is_json:  # Handling JSON request
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            role = data.get('role')
            hashed_password = generate_password_hash(password)

            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if user already exists
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                return jsonify({'error': "User already exists!"}), 400

            # Insert new user
            cursor.execute(
                "INSERT INTO users (username, email, password, role, user_status) VALUES (%s, %s, %s, %s, %s)",
                (username, email, hashed_password, role, 'active')
            )
            conn.commit()
            cursor.close()
            conn.close()

            return jsonify({'message': 'User created successfully!'}), 201

        else:  # Handling form submission (if necessary)
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            role = request.form['role']
            hashed_password = generate_password_hash(password)

            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if user already exists
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                return render_template('signup.html', error="User already exists!")

            # Insert new user
            cursor.execute(
                "INSERT INTO users (username, email, password, role, user_status) VALUES (%s, %s, %s, %s, %s)",
                (username, email, hashed_password, role, 'active')
            )
            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('auth.login_page'))

    return render_template('signup.html')

# Dashboard (Protected)
@auth_bp.route('/dashboard', methods=['GET'])
@token_required
def dashboard(current_user):
    if current_user['role'] == 'patient':
        return render_template('patient-user-dashboard.html', user=current_user)
    elif current_user['role'] == 'doctor':
        return render_template('doctor-user-dashboard.html', user=current_user)
    elif current_user['role'] == 'admin':
        return render_template('admin-user-dashboard.html', user=current_user)
    else:
        return redirect(url_for('auth.login_page'))

# Logout
@auth_bp.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for('auth.login_page'))


@auth_bp.route('/api/check-auth')
def check_auth():
    token = session.get('token')
    if token:
        try:
            jwt.decode(token, 'd28ab6f8995286e60aed281a574c18a03ff99490de1ab1f6', algorithms=["HS256"])
            return jsonify({'isAuthenticated': True})
        except jwt.ExpiredSignatureError:
            session.pop('token', None)  # Remove expired token
        except jwt.InvalidTokenError:
            session.pop('token', None)  # Remove invalid token

    return jsonify({'isAuthenticated': False})
