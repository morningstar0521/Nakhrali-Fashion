from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin', methods=['GET'])
@jwt_required()
@admin_required
def admin_dashboard():
    return jsonify({'message': 'Admin access granted'}), 200
from flask import Blueprint, request, jsonify
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def get_dashboard():
    """Get admin dashboard data"""
    return jsonify({'message': 'Admin dashboard endpoint'}), 200 