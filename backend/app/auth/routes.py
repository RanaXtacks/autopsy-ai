from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, get_jwt, 
    create_access_token, set_access_cookies
)
import logging
from datetime import datetime, timezone
from app.services import AuthService
from app.validators import AuthValidator
from . import auth_bp
from .decorators import require_ownership # placeholder if needed

logger = logging.getLogger(__name__)
auth_service = AuthService()

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    POST /api/auth/register
    """
    data = request.get_json() or {}
    
    # Validate input
    is_valid, error_msg = AuthValidator.validate_registration(data)
    if not is_valid:
        return jsonify({'success': False, 'message': error_msg}), 400
    
    user, error = auth_service.register_user(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    
    if error:
        return jsonify({'success': False, 'message': error}), 400
    
    return jsonify({
        'success': True,
        'message': 'User registered successfully',
        'data': {'user': user.to_dict()}
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login a user
    POST /api/auth/login
    """
    data = request.get_json() or {}
    
    # Validate input
    is_valid, error_msg = AuthValidator.validate_login(data)
    if not is_valid:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    access_token, refresh_token, user, error = auth_service.login_user(
        email=data['email'],
        password=data['password']
    )
    
    if error or not user:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token
    POST /api/auth/refresh
    """
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({
        'success': True,
        'access_token': new_access_token
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout a user (revoke access token)
    POST /api/auth/logout
    """
    jwt_data = get_jwt()
    jti = jwt_data['jti']
    token_type = jwt_data['type']
    
    # Get expiration from jwt payload. 'exp' is a unix timestamp.
    expires = datetime.fromtimestamp(jwt_data['exp'], timezone.utc)
    current_user_id = int(get_jwt_identity())
    
    success = auth_service.revoke_token(jti, token_type, current_user_id, expires)
    
    if success:
        return jsonify({'success': True, 'message': 'Successfully logged out'}), 200
    else:
        return jsonify({'success': False, 'message': 'Could not log out'}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current user profile
    GET /api/auth/me
    """
    current_user_id = get_jwt_identity()
    user = auth_service.get_user_profile(int(current_user_id))
    
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
        
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat() if user.created_at else None
    }), 200


@auth_bp.route('/profile/<int:user_id>', methods=['GET'])
@jwt_required()
def get_profile(user_id):
    """
    Get user profile (requires authentication)
    GET /api/auth/profile/<user_id>
    """
    user = auth_service.get_user_profile(user_id)
    
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    return jsonify({
        'success': True,
        'data': {'user': user.to_dict()}
    }), 200
