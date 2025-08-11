from flask import Blueprint, request, jsonify
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def get_dashboard():
    """Get admin dashboard data"""
    return jsonify({'message': 'Admin dashboard endpoint'}), 200 