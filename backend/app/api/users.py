from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User, UserAddress, UserProfile
from app.utils.decorators import handle_errors, validate_json
from app.utils.validators import validate_uuid, validate_phone
import uuid

users_bp = Blueprint('users', __name__)

@users_bp.route('/addresses', methods=['GET'])
@jwt_required()
@handle_errors
def get_addresses():
    """Get user addresses"""
    try:
        current_user_id = get_jwt_identity()
        addresses = UserAddress.query.filter_by(user_id=current_user_id).all()
        
        return jsonify({
            'addresses': [address.to_dict() for address in addresses]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get addresses error: {str(e)}")
        return jsonify({'error': 'Failed to fetch addresses'}), 500

@users_bp.route('/addresses', methods=['POST'])
@jwt_required()
@handle_errors
@validate_json('first_name', 'last_name', 'phone', 'address_line1', 'city', 'state', 'postal_code')
def add_address():
    """Add new address"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate phone
        if not validate_phone(data['phone']):
            return jsonify({'error': 'Invalid phone number format'}), 400
        
        address = UserAddress(
            user_id=current_user_id,
            address_type=data.get('address_type', 'delivery'),
            is_default=data.get('is_default', False),
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data['phone'],
            address_line1=data['address_line1'],
            address_line2=data.get('address_line2'),
            city=data['city'],
            state=data['state'],
            postal_code=data['postal_code'],
            country=data.get('country', 'India'),
            landmark=data.get('landmark')
        )
        
        # If this is set as default, unset other defaults
        if address.is_default:
            UserAddress.query.filter_by(
                user_id=current_user_id, 
                is_default=True
            ).update({'is_default': False})
        
        db.session.add(address)
        db.session.commit()
        
        return jsonify({
            'message': 'Address added successfully',
            'address': address.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Add address error: {str(e)}")
        return jsonify({'error': 'Failed to add address'}), 500

@users_bp.route('/addresses/<address_id>', methods=['PUT'])
@jwt_required()
@handle_errors
def update_address(address_id):
    """Update address"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not validate_uuid(address_id):
            return jsonify({'error': 'Invalid address ID'}), 400
        
        address = UserAddress.query.filter_by(
            id=address_id, 
            user_id=current_user_id
        ).first()
        
        if not address:
            return jsonify({'error': 'Address not found'}), 404
        
        # Update fields
        for field in ['first_name', 'last_name', 'phone', 'address_line1', 
                     'address_line2', 'city', 'state', 'postal_code', 
                     'country', 'landmark', 'address_type']:
            if field in data:
                setattr(address, field, data[field])
        
        # Handle default address
        if data.get('is_default', False):
            UserAddress.query.filter_by(
                user_id=current_user_id, 
                is_default=True
            ).update({'is_default': False})
            address.is_default = True
        
        db.session.commit()
        
        return jsonify({
            'message': 'Address updated successfully',
            'address': address.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update address error: {str(e)}")
        return jsonify({'error': 'Failed to update address'}), 500

@users_bp.route('/addresses/<address_id>', methods=['DELETE'])
@jwt_required()
@handle_errors
def delete_address(address_id):
    """Delete address"""
    try:
        current_user_id = get_jwt_identity()
        
        if not validate_uuid(address_id):
            return jsonify({'error': 'Invalid address ID'}), 400
        
        address = UserAddress.query.filter_by(
            id=address_id, 
            user_id=current_user_id
        ).first()
        
        if not address:
            return jsonify({'error': 'Address not found'}), 404
        
        db.session.delete(address)
        db.session.commit()
        
        return jsonify({'message': 'Address deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Delete address error: {str(e)}")
        return jsonify({'error': 'Failed to delete address'}), 500 