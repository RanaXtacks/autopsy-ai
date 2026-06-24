from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request

def require_role(role):
    """
    Decorator to ensure the current user has a specific role.
    This acts as a placeholder/ready-to-use architecture component 
    for future role-based access control.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") == role:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403
        return decorator
    return wrapper

def require_ownership():
    """
    Decorator to validate if the current user owns the requested resource.
    Can be expanded based on specific resource endpoints.
    """
    pass
