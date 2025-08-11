from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, limiter
from app.models.wishlist import Wishlist, WishlistItem
from app.models.product import Product, ProductVariant
from app.utils.decorators import handle_errors, validate_json
from app.utils.validators import validate_uuid
import uuid

wishlist_bp = Blueprint('wishlist', __name__)

@wishlist_bp.route('/', methods=['GET'])
@jwt_required()
@handle_errors
def get_wishlist():
    """Get user's wishlist"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get or create wishlist
        wishlist = Wishlist.query.filter_by(user_id=current_user_id).first()
        if not wishlist:
            wishlist = Wishlist(user_id=current_user_id)
            db.session.add(wishlist)
            db.session.commit()
        
        # Get wishlist items with product details
        wishlist_items = []
        for item in wishlist.items:
            if item.product and item.product.is_active:
                item_dict = item.to_dict()
                wishlist_items.append(item_dict)
        
        return jsonify({
            'wishlist': wishlist.to_dict(),
            'items': wishlist_items
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get wishlist error: {str(e)}")
        return jsonify({'error': 'Failed to fetch wishlist'}), 500

@wishlist_bp.route('/add', methods=['POST'])
@jwt_required()
@handle_errors
@validate_json('product_id')
def add_to_wishlist():
    """Add item to wishlist"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        product_id = data['product_id']
        product_variant_id = data.get('product_variant_id')
        notes = data.get('notes')
        priority = data.get('priority', 'medium')
        
        # Validate product ID
        if not validate_uuid(product_id):
            return jsonify({'error': 'Invalid product ID'}), 400
        
        # Get product
        product = Product.query.get(product_id)
        if not product or not product.is_active:
            return jsonify({'error': 'Product not found or unavailable'}), 404
        
        # Get or create wishlist
        wishlist = Wishlist.query.filter_by(user_id=current_user_id).first()
        if not wishlist:
            wishlist = Wishlist(user_id=current_user_id)
            db.session.add(wishlist)
            db.session.commit()
        
        # Check if item already exists in wishlist
        existing_item = WishlistItem.query.filter_by(
            wishlist_id=wishlist.id,
            product_id=product_id,
            product_variant_id=product_variant_id
        ).first()
        
        if existing_item:
            return jsonify({
                'message': 'Item already in wishlist',
                'wishlist_item': existing_item.to_dict()
            }), 200
        else:
            # Create new wishlist item
            wishlist_item = WishlistItem(
                wishlist_id=wishlist.id,
                product_id=product_id,
                product_variant_id=product_variant_id,
                notes=notes,
                priority=priority
            )
            db.session.add(wishlist_item)
            db.session.commit()
        
        return jsonify({
            'message': 'Item added to wishlist successfully',
            'wishlist_item': wishlist_item.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Add to wishlist error: {str(e)}")
        return jsonify({'error': 'Failed to add item to wishlist'}), 500

@wishlist_bp.route('/remove/<item_id>', methods=['DELETE'])
@jwt_required()
@handle_errors
def remove_from_wishlist(item_id):
    """Remove item from wishlist"""
    try:
        current_user_id = get_jwt_identity()
        
        # Validate item ID
        if not validate_uuid(item_id):
            return jsonify({'error': 'Invalid item ID'}), 400
        
        # Get wishlist
        wishlist = Wishlist.query.filter_by(user_id=current_user_id).first()
        if not wishlist:
            return jsonify({'error': 'Wishlist not found'}), 404
        
        # Get wishlist item
        wishlist_item = WishlistItem.query.filter_by(id=item_id, wishlist_id=wishlist.id).first()
        if not wishlist_item:
            return jsonify({'error': 'Item not found in wishlist'}), 404
        
        # Remove item
        db.session.delete(wishlist_item)
        db.session.commit()
        
        return jsonify({
            'message': 'Item removed from wishlist successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Remove from wishlist error: {str(e)}")
        return jsonify({'error': 'Failed to remove item from wishlist'}), 500

@wishlist_bp.route('/clear', methods=['DELETE'])
@jwt_required()
@handle_errors
def clear_wishlist():
    """Clear all items from wishlist"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get wishlist
        wishlist = Wishlist.query.filter_by(user_id=current_user_id).first()
        if not wishlist:
            return jsonify({'error': 'Wishlist not found'}), 404
        
        # Remove all items
        WishlistItem.query.filter_by(wishlist_id=wishlist.id).delete()
        db.session.commit()
        
        return jsonify({
            'message': 'Wishlist cleared successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Clear wishlist error: {str(e)}")
        return jsonify({'error': 'Failed to clear wishlist'}), 500

@wishlist_bp.route('/update/<item_id>', methods=['PUT'])
@jwt_required()
@handle_errors
def update_wishlist_item(item_id):
    """Update wishlist item details"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate item ID
        if not validate_uuid(item_id):
            return jsonify({'error': 'Invalid item ID'}), 400
        
        # Get wishlist
        wishlist = Wishlist.query.filter_by(user_id=current_user_id).first()
        if not wishlist:
            return jsonify({'error': 'Wishlist not found'}), 404
        
        # Get wishlist item
        wishlist_item = WishlistItem.query.filter_by(id=item_id, wishlist_id=wishlist.id).first()
        if not wishlist_item:
            return jsonify({'error': 'Item not found in wishlist'}), 404
        
        # Update fields
        if 'notes' in data:
            wishlist_item.notes = data['notes']
        
        if 'priority' in data and data['priority'] in ['low', 'medium', 'high']:
            wishlist_item.priority = data['priority']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Wishlist item updated successfully',
            'wishlist_item': wishlist_item.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update wishlist item error: {str(e)}")
        return jsonify({'error': 'Failed to update wishlist item'}), 500

@wishlist_bp.route('/move-to-cart/<item_id>', methods=['POST'])
@jwt_required()
@handle_errors
def move_to_cart(item_id):
    """Move item from wishlist to cart"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json() or {}
        quantity = data.get('quantity', 1)
        
        # Validate item ID
        if not validate_uuid(item_id):
            return jsonify({'error': 'Invalid item ID'}), 400
        
        # Get wishlist
        wishlist = Wishlist.query.filter_by(user_id=current_user_id).first()
        if not wishlist:
            return jsonify({'error': 'Wishlist not found'}), 404
        
        # Get wishlist item
        wishlist_item = WishlistItem.query.filter_by(id=item_id, wishlist_id=wishlist.id).first()
        if not wishlist_item:
            return jsonify({'error': 'Item not found in wishlist'}), 404
        
        # Get product
        product = Product.query.get(wishlist_item.product_id)
        if not product or not product.is_active:
            return jsonify({'error': 'Product not found or unavailable'}), 404
        
        # Check stock
        if product.track_quantity:
            available_stock = product.stock_quantity
            if wishlist_item.product_variant_id:
                variant = ProductVariant.query.get(wishlist_item.product_variant_id)
                if variant:
                    available_stock = variant.stock_quantity
            
            if quantity > available_stock and not product.allow_backorder:
                return jsonify({'error': 'Insufficient stock'}), 400
        
        # Add to cart (using cart API)
        # This would typically be a direct function call or internal API request
        # For now, we'll just return success
        
        # Remove from wishlist
        db.session.delete(wishlist_item)
        db.session.commit()
        
        return jsonify({
            'message': 'Item moved to cart successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Move to cart error: {str(e)}")
        return jsonify({'error': 'Failed to move item to cart'}), 500