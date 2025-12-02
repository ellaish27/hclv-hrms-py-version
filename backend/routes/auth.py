from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import db, User
from datetime import datetime, timedelta
import bcrypt as pybcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not pybcrypt.checkpw(password.encode(), user.password_hash.encode()):
        if user:
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 5:
                user.is_locked = True
                user.locked_until = datetime.utcnow() + timedelta(minutes=30)
            db.session.commit()
        return jsonify({'error': 'Invalid credentials'}), 401

    if user.is_locked:
        return jsonify({'error': 'Account locked'}), 403

    user.failed_login_attempts = 0
    db.session.commit()

    token = create_access_token(identity={'id': user.id, 'role': user.role, 'email': user.email})
    return jsonify({'token': token, 'user': {'id': user.id, 'role': user.role}})
