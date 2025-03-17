import requests
from flask import request, jsonify

AUTH_SERVICE_URL = "http://127.0.0.1:5005/api/auth/validate_token"

def token_required(func):
    """Decorator to validate JWT token via `auth_service` API."""
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")  # Get token from headers

        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        try:
            # Send request to auth_service for validation
            response = requests.post(AUTH_SERVICE_URL, json={"token": token.replace("Bearer ", "")})

            if response.status_code == 200:
                current_user = response.json()  # User details from auth service
                return func(current_user, *args, **kwargs)
            else:
                return jsonify({"error": "Invalid or expired token"}), 401
        except requests.exceptions.RequestException:
            return jsonify({"error": "Auth service unavailable"}), 503

    wrapper.__name__ = func.__name__
    return wrapper
