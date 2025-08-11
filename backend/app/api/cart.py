from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, limiter
from app.models.cart import Cart, CartItem
from app.models.product import Product, ProductVariant
from app.models.coupon import Coupon
from app.utils.decorators import handle_errors, validate_json
from app.utils.validators import validate_uuid, validate_quantity
import uuid

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/', methods=['GET'])
@jwt_required()
@handle_errors
def get_cart():
    """Get user's cart"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get or create cart
        cart = Cart.query.filter_by(user_id=current_user_id, is_active=True).first()
        if not cart:
            cart = Cart(user_id=current_user_id)
            db.session.add(cart)
            db.session.commit()
        
        # Calculate totals
        totals = cart.calculate_totals()
        
        # Get cart items with product details
        cart_items = []
        for item in cart.items:
            item_dict = item.to_dict()
            cart_items.append(item_dict)
        
        return jsonify({
            'cart': cart.to_dict(),
            'items': cart_items,
            'totals': totals
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get cart error: {str(e)}")
        return jsonify({'error': 'Failed to fetch cart'}), 500

@cart_bp.route('/add', methods=['POST'])
@jwt_required()
@handle_errors
@validate_json('product_id', 'quantity')
def add_to_cart():
    """Add item to cart"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        product_id = data['product_id']
        quantity = data['quantity']
        product_variant_id = data.get('product_variant_id')
        selected_variant_name = data.get('selected_variant_name')
        selected_variant_value = data.get('selected_variant_value')
        
        # Validate product ID
        if not validate_uuid(product_id):
            return jsonify({'error': 'Invalid product ID'}), 400
        
        # Validate quantity
        if not validate_quantity(quantity):
            return jsonify({'error': 'Invalid quantity'}), 400
        
        # Get product
        product = Product.query.get(product_id)
        if not product or not product.is_active:
            return jsonify({'error': 'Product not found or unavailable'}), 404
        
        # Check stock
        if product.track_quantity:
            available_stock = product.stock_quantity
            if product_variant_id:
                variant = ProductVariant.query.get(product_variant_id)
                if variant:
                    available_stock = variant.stock_quantity
            
            if quantity > available_stock and not product.allow_backorder:
                return jsonify({'error': 'Insufficient stock'}), 400
        
        # Get or create cart
        cart = Cart.query.filter_by(user_id=current_user_id, is_active=True).first()
        if not cart:
            cart = Cart(user_id=current_user_id)
            db.session.add(cart)
            db.session.commit()
        
        # Check if item already exists in cart
        existing_item = CartItem.query.filter_by(
            cart_id=cart.id,
            product_id=product_id,
            product_variant_id=product_variant_id
        ).first()
        
        if existing_item:
            # Update quantity
            new_quantity = existing_item.quantity + quantity
            if not existing_item.update_quantity(new_quantity):
                return jsonify({'error': 'Failed to update quantity'}), 400
        else:
            # Create new cart item
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                product_variant_id=product_variant_id,
                quantity=quantity,
                unit_price=product.price,
                selected_variant_name=selected_variant_name,
                selected_variant_value=selected_variant_value
            )
            db.session.add(cart_item)
        
        # Calculate totals
        cart.calculate_totals()
        db.session.commit()
        
        return jsonify({
            'message': 'Item added to cart successfully',
            'cart': cart.to_dict(),
            'totals': cart.calculate_totals()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Add to cart error: {str(e)}")
        return jsonify({'error': 'Failed to add item to cart'}), 500

@cart_bp.route('/update/<item_id>', methods=['PUT'])
@jwt_required()
@handle_errors
@validate_json('quantity')
def update_cart_item(item_id):
    """Update cart item quantity"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        quantity = data['quantity']
        
        # Validate item ID
        if not validate_uuid(item_id):
            return jsonify({'error': 'Invalid item ID'}), 400
        
        # Get cart item
        cart_item = CartItem.query.join(Cart).filter(
            CartItem.id == item_id,
            Cart.user_id == current_user_id
        ).first()
        
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), 404
        
        # Update quantity
        if not cart_item.update_quantity(quantity):
            return jsonify({'error': 'Failed to update quantity'}), 400
        
        # Recalculate cart totals
        cart_item.cart.calculate_totals()
        db.session.commit()
        
        return jsonify({
            'message': 'Cart item updated successfully',
            'cart': cart_item.cart.to_dict(),
            'totals': cart_item.cart.calculate_totals()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update cart item error: {str(e)}")
        return jsonify({'error': 'Failed to update cart item'}), 500

@cart_bp.route('/remove/<item_id>', methods=['DELETE'])
@jwt_required()
@handle_errors
def remove_from_cart(item_id):
    """Remove item from cart"""
    try:
        current_user_id = get_jwt_identity()
        
        # Validate item ID
        if not validate_uuid(item_id):
            return jsonify({'error': 'Invalid item ID'}), 400
        
        # Get cart item
        cart_item = CartItem.query.join(Cart).filter(
            CartItem.id == item_id,
            Cart.user_id == current_user_id
        ).first()
        
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), 404
        
        cart = cart_item.cart
        db.session.delete(cart_item)
        
        # Recalculate cart totals
        cart.calculate_totals()
        db.session.commit()
        
        return jsonify({
            'message': 'Item removed from cart successfully',
            'cart': cart.to_dict(),
            'totals': cart.calculate_totals()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Remove from cart error: {str(e)}")
        return jsonify({'error': 'Failed to remove item from cart'}), 500

@cart_bp.route('/clear', methods=['DELETE'])
@jwt_required()
@handle_errors
def clear_cart():
    """Clear all items from cart"""
    try:
        current_user_id = get_jwt_identity()
        
        cart = Cart.query.filter_by(user_id=current_user_id, is_active=True).first()
        if not cart:
            return jsonify({'message': 'Cart is already empty'}), 200
        
        cart.clear()
        db.session.commit()
        
        return jsonify({
            'message': 'Cart cleared successfully',
            'cart': cart.to_dict(),
            'totals': cart.calculate_totals()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Clear cart error: {str(e)}")
        return jsonify({'error': 'Failed to clear cart'}), 500

@cart_bp.route('/apply-coupon', methods=['POST'])
@jwt_required()
@handle_errors
@validate_json('coupon_code')
def apply_coupon():
    """Apply coupon to cart"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        coupon_code = data['coupon_code']
        
        # Get cart
        cart = Cart.query.filter_by(user_id=current_user_id, is_active=True).first()
        if not cart:
            return jsonify({'error': 'Cart not found'}), 404
        
        # Get coupon
        coupon = Coupon.query.filter_by(code=coupon_code.upper()).first()
        if not coupon:
            return jsonify({'error': 'Invalid coupon code'}), 400
        
        # Validate coupon
        if not coupon.is_valid():
            return jsonify({'error': 'Coupon is not valid'}), 400
        
        # Check minimum order amount
        if cart.subtotal < coupon.min_order_amount:
            return jsonify({'error': f'Minimum order amount of ₹{coupon.min_order_amount} required'}), 400
        
        # Check usage limits
        if coupon.max_uses and coupon.current_uses >= coupon.max_uses:
            return jsonify({'error': 'Coupon usage limit exceeded'}), 400
        
        # Check if user has already used this coupon
        from app.models.coupon import CouponUsage
        user_usage = CouponUsage.query.filter_by(
            coupon_id=coupon.id,
            user_id=current_user_id
        ).count()
        
        if user_usage >= coupon.max_uses_per_user:
            return jsonify({'error': 'You have already used this coupon'}), 400
        
        # Apply coupon
        cart.coupon_code = coupon.code
        cart.coupon_discount = coupon.calculate_discount(cart.subtotal)
        
        # Recalculate totals
        cart.calculate_totals()
        db.session.commit()
        
        return jsonify({
            'message': 'Coupon applied successfully',
            'cart': cart.to_dict(),
            'totals': cart.calculate_totals(),
            'coupon': coupon.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Apply coupon error: {str(e)}")
        return jsonify({'error': 'Failed to apply coupon'}), 500

@cart_bp.route('/remove-coupon', methods=['DELETE'])
@jwt_required()
@handle_errors
def remove_coupon():
    """Remove coupon from cart"""
    try:
        current_user_id = get_jwt_identity()
        
        cart = Cart.query.filter_by(user_id=current_user_id, is_active=True).first()
        if not cart:
            return jsonify({'error': 'Cart not found'}), 404
        
        cart.coupon_code = None
        cart.coupon_discount = 0
        
        # Recalculate totals
        cart.calculate_totals()
        db.session.commit()
        
        return jsonify({
            'message': 'Coupon removed successfully',
            'cart': cart.to_dict(),
            'totals': cart.calculate_totals()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Remove coupon error: {str(e)}")
        return jsonify({'error': 'Failed to remove coupon'}), 500

@cart_bp.route('/validate', methods=['GET'])
@jwt_required()
@handle_errors
def validate_cart():
    """Validate cart items for checkout"""
    try:
        current_user_id = get_jwt_identity()
        
        cart = Cart.query.filter_by(user_id=current_user_id, is_active=True).first()
        if not cart:
            return jsonify({'error': 'Cart not found'}), 404
        
        validation_errors = []
        warnings = []
        
        for item in cart.items:
            # Check if product is still available
            if not item.is_available():
                validation_errors.append({
                    'item_id': str(item.id),
                    'product_id': str(item.product_id),
                    'error': 'Product is no longer available'
                })
                continue
            
            # Check stock
            if item.product and item.product.track_quantity:
                available_stock = item.product.stock_quantity
                if item.product_variant:
                    available_stock = item.product_variant.stock_quantity
                
                if item.quantity > available_stock and not item.product.allow_backorder:
                    validation_errors.append({
                        'item_id': str(item.id),
                        'product_id': str(item.product_id),
                        'error': f'Only {available_stock} items available in stock'
                    })
                elif item.quantity > available_stock:
                    warnings.append({
                        'item_id': str(item.id),
                        'product_id': str(item.product_id),
                        'warning': f'Only {available_stock} items available, rest will be backordered'
                    })
        
        return jsonify({
            'is_valid': len(validation_errors) == 0,
            'errors': validation_errors,
            'warnings': warnings
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Validate cart error: {str(e)}")
        return jsonify({'error': 'Failed to validate cart'}), 500 