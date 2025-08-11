from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models.user import User

def admin_required(fn):
    """Decorator to require admin role"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_admin():
            return jsonify({'error': 'Admin access required'}), 403
        
        return fn(*args, **kwargs)
    return wrapper

def superadmin_required(fn):
    """Decorator to require superadmin role"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or user.role != 'superadmin':
            return jsonify({'error': 'Superadmin access required'}), 403
        
        return fn(*args, **kwargs)
    return wrapper

def verified_user_required(fn):
    """Decorator to require verified user"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_verified:
            return jsonify({'error': 'Email verification required'}), 403
        
        return fn(*args, **kwargs)
    return wrapper

def handle_errors(fn):
    """Decorator to handle common errors"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except KeyError as e:
            return jsonify({'error': f'Missing required field: {str(e)}'}), 400
        except Exception as e:
            from flask import current_app
            current_app.logger.error(f"Unexpected error in {fn.__name__}: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    return wrapper

def validate_json(*required_fields):
    """Decorator to validate JSON request with required fields"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return jsonify({'error': 'Content-Type must be application/json'}), 400
            
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Invalid JSON data'}), 400
            
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def paginate_response(fn):
    """Decorator to handle pagination"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Limit per_page to prevent abuse
        if per_page > 100:
            per_page = 100
        
        kwargs['page'] = page
        kwargs['per_page'] = per_page
        
        return fn(*args, **kwargs)
    return wrapper

def cache_response(timeout=300):
    """Decorator to cache response (placeholder for Redis implementation)"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # In a real implementation, you'd check Redis cache here
            # For now, we'll just call the function
            return fn(*args, **kwargs)
        return wrapper
    return decorator 