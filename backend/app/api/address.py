from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import UserAddress
from app.utils.validators import validate_address_data
from app.utils.otp import send_otp, verify_otp # Assuming you have an otp utility
import uuid

address_bp = Blueprint('address', __name__, url_prefix='/addresses')

@address_bp.route('/', methods=['POST'])
@jwt_required()
def add_address():
    """Add a new address for the current user."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        if not validate_address_data(data): # Assuming validate_address_data exists
            return jsonify({'error': 'Invalid address data'}), 400

        new_address = UserAddress(user_id=current_user_id, **data)
        db.session.add(new_address)
        db.session.commit()

        return jsonify({'message': 'Address added successfully', 'address': new_address.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@address_bp.route('/', methods=['GET'])
@jwt_required()
def get_addresses():
    """Get all addresses for the current user."""
    try:
        current_user_id = get_jwt_identity()
        addresses = UserAddress.query.filter_by(user_id=current_user_id).all()
        return jsonify({'addresses': [address.to_dict() for address in addresses]}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@address_bp.route('/<uuid:address_id>', methods=['PUT'])
@jwt_required()
def update_address(address_id):
    """Update an existing address."""
    try:
        current_user_id = get_jwt_identity()
        address = UserAddress.query.filter_by(id=address_id, user_id=current_user_id).first()

        if not address:
            return jsonify({'error': 'Address not found or does not belong to the user'}), 404

        data = request.get_json()
        if not validate_address_data(data, partial=True): # Assuming partial updates are allowed
            return jsonify({'error': 'Invalid address data'}), 400

        for key, value in data.items():
            if hasattr(address, key):
                setattr(address, key, value)

        db.session.commit()
        return jsonify({'message': 'Address updated successfully', 'address': address.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@address_bp.route('/<uuid:address_id>', methods=['DELETE'])
@jwt_required()
def delete_address(address_id):
    """Delete an address."""
    try:
        current_user_id = get_jwt_identity()
        address = UserAddress.query.filter_by(id=address_id, user_id=current_user_id).first()

        if not address:
            return jsonify({'error': 'Address not found or does not belong to the user'}), 404

        db.session.delete(address)
        db.session.commit()
        return jsonify({'message': 'Address deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@address_bp.route('/<uuid:address_id>/set_default', methods=['PUT'])
@jwt_required()
def set_default_address(address_id):
    """Set an address as the default shipping or billing address."""
    try:
        current_user_id = get_jwt_identity()
        address = UserAddress.query.filter_by(id=address_id, user_id=current_user_id).first()

        if not address:
            return jsonify({'error': 'Address not found or does not belong to the user'}), 404

        address_type = request.get_json().get('address_type')
        if address_type not in ['shipping', 'billing']:
             return jsonify({'error': 'Invalid address type specified'}), 400


        # Unset the previous default address of the same type
        current_default = UserAddress.query.filter_by(
            user_id=current_user_id,
            address_type=address_type,
            is_default=True
        ).first()

        if current_default:
            current_default.is_default = False

        # Set the new default
        address.is_default = True
        address.address_type = address_type # Ensure type is set correctly

        db.session.commit()
        return jsonify({'message': f'Address set as default {address_type} successfully', 'address': address.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@address_bp.route('/send_otp', methods=['POST'])
@jwt_required()
def send_otp_for_address_verification():
    """Send an OTP to the user's phone number for address verification (Placeholder)."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        phone_number = data.get('phone_number')

        if not phone_number:
            return jsonify({'error': 'Phone number is required'}), 400

        # Placeholder for actual OTP sending logic
        # You would generate an OTP, store it with an expiry, and send it via SMS/email
        # For example:
        # otp = generate_otp()
        # save_otp(user_id, otp, expiry_time)
        # send_sms(phone_number, f'Your verification code is {otp}')

        print(f"Placeholder: Sending OTP to {phone_number} for user {current_user_id}") # Log for demonstration

        return jsonify({'message': 'OTP sent to your phone number (placeholder)'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@address_bp.route('/verify_otp', methods=['POST'])
@jwt_required()
def verify_address_otp():
    """Verify the OTP entered by the user (Placeholder)."""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        phone_number = data.get('phone_number')
        otp = data.get('otp')

        if not phone_number or not otp:
            return jsonify({'error': 'Phone number and OTP are required'}), 400

        # Placeholder for actual OTP verification logic
        # You would retrieve the stored OTP for the user and compare it
        # is_valid = check_otp(user_id, otp)
        # if is_valid:
        #    mark_address_as_verified(address_id) # Assuming OTP is tied to an address or phone number

        print(f"Placeholder: Verifying OTP {otp} for phone {phone_number} for user {current_user_id}") # Log for demonstration

        # Assume verification is successful for placeholder
        is_valid = True # Replace with actual verification logic

        if is_valid:
             return jsonify({'message': 'OTP verified successfully (placeholder)'}), 200
        else:
            return jsonify({'error': 'Invalid OTP'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500