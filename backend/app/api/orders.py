from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, limiter
from app.models.order import Order, OrderItem, OrderStatus
from app.models.cart import Cart, CartItem
from app.models.user import User, UserAddress
from app.models.payment import Payment
from app.utils.decorators import handle_errors, validate_json, admin_required
from app.utils.validators import validate_uuid
from datetime import datetime
import uuid

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['GET'])
@jwt_required()
@handle_errors
def get_orders():
    """Get user's orders"""
    try:
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        orders = Order.query.filter_by(user_id=current_user_id).order_by(
            Order.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        order_data = []
        for order in orders.items:
            order_dict = order.to_dict()
            order_dict['items'] = [item.to_dict() for item in order.items]
            order_data.append(order_dict)
        
        return jsonify({
            'orders': order_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': orders.total,
                'total_pages': orders.pages,
                'has_next': orders.has_next,
                'has_prev': orders.has_prev
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get orders error: {str(e)}")
        return jsonify({'error': 'Failed to fetch orders'}), 500

@orders_bp.route('/<order_id>', methods=['GET'])
@jwt_required()
@handle_errors
def get_order(order_id):
    """Get specific order details"""
    try:
        current_user_id = get_jwt_identity()
        
        if not validate_uuid(order_id):
            return jsonify({'error': 'Invalid order ID'}), 400
        
        order = Order.query.filter_by(id=order_id, user_id=current_user_id).first()
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        order_dict = order.to_dict()
        order_dict['items'] = [item.to_dict() for item in order.items]
        
        # Add addresses
        if order.shipping_address_id:
            shipping_address = UserAddress.query.get(order.shipping_address_id)
            order_dict['shipping_address'] = shipping_address.to_dict() if shipping_address else None
        
        if order.billing_address_id:
            billing_address = UserAddress.query.get(order.billing_address_id)
            order_dict['billing_address'] = billing_address.to_dict() if billing_address else None
        
        # Add payments
        payments = Payment.query.filter_by(order_id=order_id).all()
        order_dict['payments'] = [payment.to_dict() for payment in payments]
        
        return jsonify({'order': order_dict}), 200
        
    except Exception as e:
        current_app.logger.error(f"Get order error: {str(e)}")
        return jsonify({'error': 'Failed to fetch order'}), 500

@orders_bp.route('/create', methods=['POST'])
@jwt_required()
@handle_errors
@validate_json('shipping_address_id', 'payment_method')
def create_order():
    """Create new order from cart"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Get user's cart
        cart = Cart.query.filter_by(user_id=current_user_id, is_active=True).first()
        if not cart or cart.items.count() == 0:
            return jsonify({'error': 'Cart is empty'}), 400
        
        # Validate addresses
        shipping_address_id = data['shipping_address_id']
        billing_address_id = data.get('billing_address_id', shipping_address_id)
        
        if not validate_uuid(shipping_address_id):
            return jsonify({'error': 'Invalid shipping address ID'}), 400
        
        if billing_address_id and not validate_uuid(billing_address_id):
            return jsonify({'error': 'Invalid billing address ID'}), 400
        
        # Verify addresses belong to user
        shipping_address = UserAddress.query.filter_by(
            id=shipping_address_id, 
            user_id=current_user_id
        ).first()
        
        if not shipping_address:
            return jsonify({'error': 'Shipping address not found'}), 404
        
        billing_address = None
        if billing_address_id != shipping_address_id:
            billing_address = UserAddress.query.filter_by(
                id=billing_address_id, 
                user_id=current_user_id
            ).first()
            
            if not billing_address:
                return jsonify({'error': 'Billing address not found'}), 404
        
        # Validate cart items
        for item in cart.items:
            if not item.is_available():
                return jsonify({'error': f'Product {item.product.name} is no longer available'}), 400
        
        # Create order
        order = Order(
            user_id=current_user_id,
            shipping_address_id=shipping_address_id,
            billing_address_id=billing_address_id,
            payment_method=data['payment_method'],
            customer_notes=data.get('customer_notes'),
            shipping_method=data.get('shipping_method', 'Standard'),
            coupon_code=cart.coupon_code
        )
        
        # Calculate totals
        order.subtotal = cart.subtotal
        order.tax_amount = cart.tax_amount
        order.shipping_amount = cart.shipping_amount
        order.discount_amount = cart.discount_amount
        order.total_amount = cart.total_amount
        
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items
        for cart_item in cart.items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                product_variant_id=cart_item.product_variant_id,
                product_name=cart_item.product.name,
                product_sku=cart_item.product.sku,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                total_price=cart_item.total_price,
                material=cart_item.product.material,
                weight=cart_item.product.weight,
                purity=cart_item.product.purity,
                variant_name=cart_item.selected_variant_name,
                variant_value=cart_item.selected_variant_value
            )
            db.session.add(order_item)
            
            # Update product stock
            if cart_item.product.track_quantity:
                if cart_item.product_variant:
                    cart_item.product_variant.stock_quantity -= cart_item.quantity
                else:
                    cart_item.product.stock_quantity -= cart_item.quantity
        
        # Clear cart
        cart.clear()
        
        # Create initial payment record
        payment = Payment(
            user_id=current_user_id,
            order_id=order.id,
            amount=order.total_amount,
            payment_method=data['payment_method'],
            payment_status='pending'
        )
        db.session.add(payment)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order created successfully',
            'order': order.to_dict(),
            'order_id': str(order.id),
            'order_number': order.order_number
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Create order error: {str(e)}")
        return jsonify({'error': 'Failed to create order'}), 500

@orders_bp.route('/<order_id>/cancel', methods=['POST'])
@jwt_required()
@handle_errors
def cancel_order(order_id):
    """Cancel order"""
    try:
        current_user_id = get_jwt_identity()
        
        if not validate_uuid(order_id):
            return jsonify({'error': 'Invalid order ID'}), 400
        
        order = Order.query.filter_by(id=order_id, user_id=current_user_id).first()
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        if not order.can_cancel():
            return jsonify({'error': 'Order cannot be cancelled'}), 400
        
        order.status = OrderStatus.CANCELLED
        order.cancelled_at = datetime.utcnow()
        
        # Restore product stock
        for item in order.items:
            if item.product.track_quantity:
                if item.product_variant:
                    item.product_variant.stock_quantity += item.quantity
                else:
                    item.product.stock_quantity += item.quantity
        
        db.session.commit()
        
        return jsonify({
            'message': 'Order cancelled successfully',
            'order': order.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Cancel order error: {str(e)}")
        return jsonify({'error': 'Failed to cancel order'}), 500

@orders_bp.route('/<order_id>/return', methods=['POST'])
@jwt_required()
@handle_errors
@validate_json('reason')
def request_return(order_id):
    """Request order return"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not validate_uuid(order_id):
            return jsonify({'error': 'Invalid order ID'}), 400
        
        order = Order.query.filter_by(id=order_id, user_id=current_user_id).first()
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        if not order.can_return():
            return jsonify({'error': 'Order cannot be returned'}), 400
        
        order.status = OrderStatus.RETURNED
        order.admin_notes = f"Return requested: {data['reason']}"
        
        db.session.commit()
        
        return jsonify({
            'message': 'Return request submitted successfully',
            'order': order.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Request return error: {str(e)}")
        return jsonify({'error': 'Failed to request return'}), 500

@orders_bp.route('/track/<order_number>', methods=['GET'])
def track_order(order_number):
    """Track order by order number (public endpoint)"""
    try:
        order = Order.query.filter_by(order_number=order_number).first()
        if not order:
            return jsonify({'error': 'Order not found'}), 404
        
        # Return limited order info for public tracking
        tracking_info = {
            'order_number': order.order_number,
            'status': order.status.value,
            'status_display': order.get_status_display(),
            'tracking_number': order.tracking_number,
            'estimated_delivery': order.estimated_delivery.isoformat() if order.estimated_delivery else None,
            'shipped_at': order.shipped_at.isoformat() if order.shipped_at else None,
            'delivered_at': order.delivered_at.isoformat() if order.delivered_at else None
        }
        
        return jsonify({'tracking_info': tracking_info}), 200
        
    except Exception as e:
        current_app.logger.error(f"Track order error: {str(e)}")
        return jsonify({'error': 'Failed to track order'}), 500 