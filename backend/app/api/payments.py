from flask import Blueprint, request, jsonify
from app.utils.decorators import handle_errors

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/create-payment', methods=['POST'])
@handle_errors
def create_payment():
    """Create payment intent"""
    return jsonify({'message': 'Payment creation endpoint'}), 200

@payments_bp.route('/webhook', methods=['POST'])
@handle_errors
def payment_webhook():
    """Handle payment webhooks"""
    return jsonify({'message': 'Payment webhook endpoint'}), 200 