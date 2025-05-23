from flask import Blueprint, request, jsonify, session, current_app
from src.models.user import db, User
from functools import wraps
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

# Decorator for verifying JWT token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if token is in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token is missing'
            }), 401
        
        try:
            # Decode token
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            
            if not current_user:
                return jsonify({
                    'success': False,
                    'message': 'Invalid token'
                }), 401
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Invalid token'
            }), 401
            
        return f(current_user, *args, **kwargs)
    
    return decorated

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
            
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({
                'success': False,
                'message': 'Invalid username or password'
            }), 401
            
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({
            'success': True,
            'token': token,
            'user': user.to_dict(),
            'message': 'Login successful'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
            
        # Check if user already exists
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'Username already exists'
            }), 400
            
        # Create new user
        new_user = User(username=data['username'])
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'user': new_user.to_dict(),
            'message': 'User registered successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    return jsonify({
        'success': True,
        'user': current_user.to_dict()
    }), 200
