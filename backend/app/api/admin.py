yesfrom flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from app.utils.decorators import admin_required
from app.utils.validators import validate_product_data
from app.models.product import Product
from app.models.order import Order, OrderStatus, OrderItem
from app.models.payment import Payment # Import Payment model
import cloudinary
import cloudinary.uploader
import cloudinary.api
from app import db
import uuid

# Ensure Product and db are imported
# from app.models.product import Product
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin', methods=['GET'])
@jwt_required()
@admin_required
def admin_dashboard():
    return jsonify({'message': 'Admin access granted'}), 200

@admin_bp.route('/admin/products', methods=['POST'])
@jwt_required()
@admin_required
def add_product():
    """Add a new product"""
    data = request.get_json()

    # Validate product data
    # Assuming validate_product_data is implemented and handles product data validation
    # if not validate_product_data(data):
    #     return jsonify({'error': 'Invalid product data'}), 400

    try:
        new_product = Product(**data)
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product added successfully', 'product': new_product.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/products/<uuid:product_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_product(product_id):
    """Delete a product"""
    product = Product.query.get(product_id)

    if not product:
        return jsonify({'error': 'Product not found'}), 404

 try:
 db.session.delete(product)
 db.session.commit()

 return jsonify({'message': 'Product deleted successfully'}), 200
 except Exception as e:
 db.session.rollback()
 return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/products/<uuid:product_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_product(product_id):
    """Update an existing product"""
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    data = request.get_json()

    # Validate updated product data
    # Assuming validate_product_data is implemented and handles product data validation
    # if not validate_product_data(data, partial=True):
    #     return jsonify({'error': 'Invalid product data'}), 400

    # Update product attributes
 try:
 for key, value in data.items():
 if hasattr(product, key):
 setattr(product, key, value)
 db.session.commit()


 return jsonify({'message': 'Product updated successfully', 'product': product.to_dict()}), 200
 except Exception as e:
 db.session.rollback()
 return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/orders/<uuid:order_id>/status', methods=['PUT'])
@jwt_required()
@admin_required
def update_order_status(order_id):
 """Update order status"""
 order = Order.query.get(order_id)
 if not order:
 return jsonify({'error': 'Order not found'}), 404

 data = request.get_json()
 new_status = data.get('status')

 if not new_status:
 return jsonify({'error': 'Status is required'}), 400

 try:
 order.status = OrderStatus[new_status.upper()]
 db.session.commit()
 return jsonify({'message': 'Order status updated successfully', 'order': order.to_dict()}), 200
 except KeyError:
 db.session.rollback()
 return jsonify({'error': f'Invalid status value: {new_status}'}), 400
 except Exception as e:
 db.session.rollback()
 return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/products/<uuid:product_id>/stock', methods=['PUT'])
@jwt_required()
@admin_required
def update_product_stock(product_id):
    """Update product stock quantity"""
    product = Product.query.get(product_id)
    if not product:

        return jsonify({'error': 'Product not found'}), 404

@admin_bp.route('/admin/orders', methods=['GET'])
@jwt_required()
@admin_required
def get_all_orders():
 """Get all orders"""

 orders = Order.query.all()
 return jsonify({'orders': [order.to_dict() for order in orders]}), 200
 data = request.get_json()
 new_status = data.get('status')

 if not new_status:
 return jsonify({'error': 'Status is required'}), 400

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def get_dashboard():
    """Get admin dashboard data"""

 return jsonify({'message': 'Admin dashboard endpoint'}), 200
 return jsonify({'message': 'Product updated successfully', 'product': product.to_dict()}), 200
    stock_data = request.get_json()
    new_stock_quantity = stock_data.get('stock_quantity')

    if not isinstance(new_stock_quantity, int) or new_stock_quantity < 0:
        return jsonify({'error': 'Invalid stock quantity. Must be a non-negative integer.'}), 400

    try:
        product.stock_quantity = new_stock_quantity
        db.session.commit()
        return jsonify({'message': 'Product stock updated successfully', 'product': product.to_dict()}), 200
    except Exception as e:
 db.session.rollback()
 return jsonify({'error': f'Invalid status value: {new_status}'}), 400
 except Exception as e: # This except block was incorrectly placed and is now removed
 db.session.rollback() # This rollback was also incorrectly placed
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/admin/upload/image', methods=['POST'])
@jwt_required()
@admin_required
def upload_image():
    """Upload image to Cloudinary"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            # Assuming you have CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET in your config
            from flask import current_app
            cloudinary.config(
                cloud_name=current_app.config.get('CLOUDINARY_CLOUD_NAME'),
                api_key=current_app.config.get('CLOUDINARY_API_KEY'),
                api_secret=current_app.config.get('CLOUDINARY_API_SECRET')
            )

            upload_result = cloudinary.uploader.upload(file)
            return jsonify({'secure_url': upload_result.get('secure_url')}), 200

        except Exception as e:
            return jsonify({'error': f'Image upload failed: {str(e)}'}), 500

    return jsonify({'error': 'File upload failed'}), 500