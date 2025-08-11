from flask import Blueprint, jsonify
from app import db
from sqlalchemy import text

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Test database connection
        db.session.execute(text('SELECT 1'))
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
    
    # Check if all required environment variables are set
    import os
    required_vars = ['DATABASE_URL', 'SECRET_KEY', 'JWT_SECRET_KEY']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    env_status = 'healthy' if not missing_vars else f'missing: {", ".join(missing_vars)}'
    
    return jsonify({
        'status': 'healthy' if db_status == 'healthy' and env_status == 'healthy' else 'unhealthy',
        'timestamp': db.func.now(),
        'database': db_status,
        'environment': env_status,
        'version': '1.0.0'
    }), 200 if db_status == 'healthy' and env_status == 'healthy' else 503

@health_bp.route('/ready', methods=['GET'])
def readiness_check():
    """Readiness check for load balancers"""
    try:
        # Test database connection
        db.session.execute(text('SELECT 1'))
        return jsonify({'status': 'ready'}), 200
    except Exception:
        return jsonify({'status': 'not ready'}), 503 