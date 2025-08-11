from flask import Blueprint, request, jsonify, current_app, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, cloudinary_client
from app.models.user import User, UserAddress, UserProfile
from app.models.wallet import Wallet, Transaction  # Assuming Wallet and Transaction models exist
from app.models.payment import Payment # Import Payment model
from app.models.notification import Notification # Assuming Notification model exists
# Assuming a SupportTicket model exists
# from app.models.support import SupportTicket
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

@users_bp.route('/wallet', methods=['GET'])
@jwt_required()
@handle_errors
def get_wallet_info():
    """Get user's wallet balance and transaction history"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Assuming user has a relationship to a Wallet model
        wallet = user.wallet # This assumes a 'wallet' relationship on the User model
        transactions = wallet.transactions if wallet else [] # Assuming a 'transactions' relationship on the Wallet model

        return jsonify({
            'balance': wallet.balance if wallet else 0.0,
            'transactions': [t.to_dict() for t in transactions] # Assuming a to_dict() method on Transaction model
        }), 200

    except Exception as e:
        current_app.logger.error(f"Get wallet info error: {str(e)}")
        return jsonify({'error': 'Failed to fetch wallet information'}), 500

@users_bp.route('/wallet/add_funds', methods=['POST'])
@jwt_required()
@handle_errors
@validate_json('amount')
def add_wallet_funds():
    """Initiate process to add funds to user's wallet"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        amount = data['amount']

        if not isinstance(amount, (int, float)) or amount <= 0:
            return jsonify({'error': 'Invalid amount'}), 400

        # Create a pending payment record for adding funds
        # This payment record is not linked to an order initially
        payment = Payment(
            user_id=current_user_id,
            amount=amount,
            payment_method='wallet_topup', # Or a specific type for wallet top-ups
            payment_status='pending',
            payment_intent_id=str(uuid.uuid4()) # Placeholder, replace with actual payment gateway intent ID
        )
        db.session.add(payment)
        db.session.commit()

        # In a real scenario, you would now interact with a payment gateway (e.g., Razorpay)
        # to create an order/payment intent for this amount.
        # The response to the frontend would include the details needed for the payment form (e.g., Razorpay order_id, key_id).
        # For now, we return a placeholder success message and the pending payment ID.
        return jsonify({
            'message': 'Wallet fund addition initiated (placeholder)',
            'payment_id': str(payment.id),
            'amount': amount,
            # Add payment gateway details here (e.g., 'razorpay_order_id', 'razorpay_key_id')
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Add wallet funds error: {str(e)}")
        return jsonify({'error': 'Failed to initiate adding wallet funds'}), 500

@users_bp.route('/profile/upload_picture', methods=['POST'])
@jwt_required()
@handle_errors
def upload_profile_picture():
    """Upload and update user's profile picture"""
    try:
        current_user_id = get_jwt_identity()

        if 'profile_picture' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['profile_picture']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file:
            upload_result = cloudinary_client.uploader.upload(
                file,
                folder=f"user_profile_pictures/{current_user_id}" # Organize uploads by user ID
            )
            secure_url = upload_result.get('secure_url')

            if not secure_url:
                return jsonify({'error': 'Failed to upload image to Cloudinary'}), 500

            user = User.query.get(current_user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404

            user_profile = user.profile # Assuming a 'profile' relationship on the User model
            if user_profile:
                user_profile.profile_picture = secure_url
                db.session.commit()

            return jsonify({'message': 'Profile picture uploaded successfully', 'url': secure_url}), 200
    except Exception as e:
        current_app.logger.error(f"Profile picture upload error: {str(e)}")
        return jsonify({'error': 'Failed to upload profile picture'}), 500

@users_bp.route('/notifications', methods=['GET'])
@jwt_required()
@handle_errors
def get_notifications():
    """Get user's notifications"""
    try:
        current_user_id = get_jwt_identity()

        # Assuming a Notification model with a user_id field
        notifications = Notification.query.filter_by(user_id=current_user_id).order_by(
            Notification.created_at.desc()
        ).all()

        return jsonify({
            'notifications': [notification.to_dict() for notification in notifications] # Assuming a to_dict() method on Notification model
        }), 200

    except Exception as e:
        current_app.logger.error(f"Get notifications error: {str(e)}")
        return jsonify({'error': 'Failed to fetch notifications'}), 500

@users_bp.route('/wallet/redeem_voucher', methods=['POST'])
@jwt_required()
@handle_errors
@validate_json('voucher_code')
def redeem_voucher():
    """Redeem a voucher and add credit to user's wallet"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        voucher_code = data['voucher_code']

        # Assuming a Voucher model with 'code', 'value', 'is_redeemed', and 'expiry_date' fields
        # from app.models.voucher import Voucher # Import Voucher model
        # voucher = Voucher.query.filter_by(code=voucher_code, is_redeemed=False).first()

        # Placeholder for voucher validation logic
        # Replace with actual database query and validation against expiry date etc.
        if voucher_code != "MYWALLETCODE10": # Example valid code
             return jsonify({'error': 'Invalid or expired voucher code'}), 400

        # Placeholder for voucher redemption logic
        # In a real application, you would get the value from the voucher object
        voucher_value = 100.00 # Example fixed value

        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Get or create wallet
        wallet = user.wallet
        if not wallet:
            wallet = Wallet(user_id=current_user_id, balance=0.0)
            db.session.add(wallet)
            db.session.flush() # Ensure wallet has an ID before creating transaction

        wallet.balance += voucher_value

        # Create transaction record (placeholder)
        # transaction = Transaction(wallet_id=wallet.id, amount=voucher_value, type='credit', description=f'Voucher redemption: {voucher_code}')
        # db.session.add(transaction)

        # Mark voucher as redeemed (placeholder)
        # voucher.is_redeemed = True

        db.session.commit()

        return jsonify({
            'message': 'Voucher redeemed successfully',
            'new_balance': wallet.balance,
            # Include transaction details in a real scenario
        }), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Redeem voucher error: {str(e)}")
        return jsonify({'error': 'Failed to redeem voucher'}), 500
        return jsonify({'error': 'Failed to initiate adding wallet funds'}), 500