from flask import Blueprint, request, jsonify
import razorpay
from app.utils.decorators import handle_errors
from flask import current_app

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/create-payment', methods=['POST'])
@handle_errors
def create_payment():
 """Create Razorpay order"""
    data = request.get_json()
    amount = data.get('amount')
    currency = data.get('currency', 'INR')
    receipt = data.get('receipt') # Optional: unique identifier for the order

 if not amount or not isinstance(amount, (int, float)) or amount <= 0:
 return jsonify({'error': 'Invalid amount'}), 400

 try:
 client = razorpay.Client(auth=(current_app.config['RAZORPAY_KEY_ID'], current_app.config['RAZORPAY_KEY_SECRET']))
 razorpay_order = client.order.create({
 'amount': int(amount * 100), # Razorpay expects amount in paise
 'currency': currency,
 'receipt': receipt or str(uuid.uuid4()) # Generate a receipt if not provided
 })
 return jsonify(razorpay_order), 201
 except Exception as e:
 return jsonify({'error': str(e)}), 500

@payments_bp.route('/webhook', methods=['POST'])
@handle_errors
def payment_webhook():
    """Handle payment webhooks"""
    return jsonify({'message': 'Payment webhook endpoint'}), 200 