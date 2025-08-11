from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, limiter
from app.models.review import Review, ReviewImage
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.utils.decorators import handle_errors, validate_json, paginate_response
from app.utils.validators import validate_uuid
from sqlalchemy import desc
import uuid

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/product/<product_id>', methods=['GET'])
@handle_errors
@paginate_response
def get_product_reviews(product_id, page=1, per_page=10):
    """Get reviews for a product"""
    try:
        # Validate product ID
        if not validate_uuid(product_id):
            return jsonify({'error': 'Invalid product ID'}), 400
        
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Get reviews
        query = Review.query.filter_by(
            product_id=product_id,
            is_approved=True
        ).order_by(desc(Review.created_at))
        
        # Apply filters
        rating = request.args.get('rating', type=int)
        if rating and 1 <= rating <= 5:
            query = query.filter_by(rating=rating)
        
        verified_only = request.args.get('verified_only', type=bool)
        if verified_only:
            query = query.filter_by(is_verified_purchase=True)
        
        has_images = request.args.get('has_images', type=bool)
        if has_images:
            query = query.filter(Review.images.any())
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        reviews = pagination.items
        
        # Get review data with user info
        review_data = []
        for review in reviews:
            review_dict = review.to_dict()
            # Add user info (name, avatar)
            if review.user:
                review_dict['user'] = {
                    'name': f"{review.user.first_name} {review.user.last_name[0]}.",
                    'avatar': review.user.profile.profile_picture if hasattr(review.user, 'profile') else None
                }
            review_data.append(review_dict)
        
        # Get rating statistics
        rating_stats = {
            'average_rating': 0,
            'total_reviews': 0,
            'rating_distribution': {
                '5': 0, '4': 0, '3': 0, '2': 0, '1': 0
            }
        }
        
        all_reviews = Review.query.filter_by(product_id=product_id, is_approved=True).all()
        if all_reviews:
            ratings = [r.rating for r in all_reviews]
            rating_stats['average_rating'] = round(sum(ratings) / len(ratings), 1)
            rating_stats['total_reviews'] = len(ratings)
            for i in range(1, 6):
                rating_stats['rating_distribution'][str(i)] = len([r for r in ratings if r == i])
        
        return jsonify({
            'reviews': review_data,
            'rating_stats': rating_stats,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'total_pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get product reviews error: {str(e)}")
        return jsonify({'error': 'Failed to fetch reviews'}), 500

@reviews_bp.route('/add', methods=['POST'])
@jwt_required()
@handle_errors
@validate_json('product_id', 'rating')
def add_review():
    """Add a new product review"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        product_id = data['product_id']
        rating = data['rating']
        title = data.get('title')
        comment = data.get('comment')
        order_id = data.get('order_id')
        images = data.get('images', [])
        
        # Validate product ID
        if not validate_uuid(product_id):
            return jsonify({'error': 'Invalid product ID'}), 400
        
        # Validate rating
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Check if user has already reviewed this product
        existing_review = Review.query.filter_by(
            user_id=current_user_id,
            product_id=product_id
        ).first()
        
        if existing_review:
            return jsonify({'error': 'You have already reviewed this product'}), 400
        
        # Check if verified purchase
        is_verified_purchase = False
        if order_id:
            if validate_uuid(order_id):
                # Check if order exists and contains this product
                order = Order.query.filter_by(
                    id=order_id,
                    user_id=current_user_id
                ).first()
                
                if order:
                    order_item = OrderItem.query.filter_by(
                        order_id=order.id,
                        product_id=product_id
                    ).first()
                    
                    if order_item:
                        is_verified_purchase = True
        else:
            # Check if user has any order with this product
            orders = Order.query.filter_by(user_id=current_user_id).all()
            for order in orders:
                order_item = OrderItem.query.filter_by(
                    order_id=order.id,
                    product_id=product_id
                ).first()
                
                if order_item:
                    is_verified_purchase = True
                    order_id = order.id
                    break
        
        # Create review
        review = Review(
            user_id=current_user_id,
            product_id=product_id,
            order_id=order_id,
            rating=rating,
            title=title,
            comment=comment,
            is_verified_purchase=is_verified_purchase,
            is_approved=True  # Auto-approve for now
        )
        
        db.session.add(review)
        db.session.flush()  # Get review ID without committing
        
        # Add images
        for image_data in images:
            if 'image_url' in image_data:
                review_image = ReviewImage(
                    review_id=review.id,
                    image_url=image_data['image_url'],
                    alt_text=image_data.get('alt_text')
                )
                db.session.add(review_image)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Review added successfully',
            'review': review.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Add review error: {str(e)}")
        return jsonify({'error': 'Failed to add review'}), 500

@reviews_bp.route('/<review_id>', methods=['PUT'])
@jwt_required()
@handle_errors
def update_review(review_id):
    """Update an existing review"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate review ID
        if not validate_uuid(review_id):
            return jsonify({'error': 'Invalid review ID'}), 400
        
        # Get review
        review = Review.query.filter_by(id=review_id, user_id=current_user_id).first()
        if not review:
            return jsonify({'error': 'Review not found or you are not authorized to update it'}), 404
        
        # Update fields
        if 'rating' in data:
            rating = data['rating']
            if not isinstance(rating, int) or not (1 <= rating <= 5):
                return jsonify({'error': 'Rating must be between 1 and 5'}), 400
            review.rating = rating
        
        if 'title' in data:
            review.title = data['title']
        
        if 'comment' in data:
            review.comment = data['comment']
        
        # Handle images
        if 'images' in data:
            # Remove existing images
            ReviewImage.query.filter_by(review_id=review.id).delete()
            
            # Add new images
            for image_data in data['images']:
                if 'image_url' in image_data:
                    review_image = ReviewImage(
                        review_id=review.id,
                        image_url=image_data['image_url'],
                        alt_text=image_data.get('alt_text')
                    )
                    db.session.add(review_image)
        
        # Reset approval if needed
        review.is_approved = True  # Auto-approve for now
        
        db.session.commit()
        
        return jsonify({
            'message': 'Review updated successfully',
            'review': review.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update review error: {str(e)}")
        return jsonify({'error': 'Failed to update review'}), 500

@reviews_bp.route('/<review_id>', methods=['DELETE'])
@jwt_required()
@handle_errors
def delete_review(review_id):
    """Delete a review"""
    try:
        current_user_id = get_jwt_identity()
        
        # Validate review ID
        if not validate_uuid(review_id):
            return jsonify({'error': 'Invalid review ID'}), 400
        
        # Get review
        review = Review.query.filter_by(id=review_id, user_id=current_user_id).first()
        if not review:
            return jsonify({'error': 'Review not found or you are not authorized to delete it'}), 404
        
        # Delete review (cascade will delete images)
        db.session.delete(review)
        db.session.commit()
        
        return jsonify({
            'message': 'Review deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Delete review error: {str(e)}")
        return jsonify({'error': 'Failed to delete review'}), 500

@reviews_bp.route('/<review_id>/helpful', methods=['POST'])
@jwt_required()
@handle_errors
def mark_review_helpful(review_id):
    """Mark a review as helpful"""
    try:
        # Validate review ID
        if not validate_uuid(review_id):
            return jsonify({'error': 'Invalid review ID'}), 400
        
        # Get review
        review = Review.query.get(review_id)
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        # Increment helpful count
        review.is_helpful += 1
        db.session.commit()
        
        return jsonify({
            'message': 'Review marked as helpful',
            'helpful_count': review.is_helpful
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Mark review helpful error: {str(e)}")
        return jsonify({'error': 'Failed to mark review as helpful'}), 500

@reviews_bp.route('/user', methods=['GET'])
@jwt_required()
@handle_errors
@paginate_response
def get_user_reviews(page=1, per_page=10):
    """Get reviews by current user"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get reviews
        query = Review.query.filter_by(
            user_id=current_user_id
        ).order_by(desc(Review.created_at))
        
        # Paginate
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        reviews = pagination.items
        
        # Get review data with product info
        review_data = []
        for review in reviews:
            review_dict = review.to_dict()
            # Add product info
            if review.product:
                review_dict['product'] = {
                    'id': str(review.product.id),
                    'name': review.product.name,
                    'main_image': review.product.main_image
                }
            review_data.append(review_dict)
        
        return jsonify({
            'reviews': review_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'total_pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get user reviews error: {str(e)}")
        return jsonify({'error': 'Failed to fetch reviews'}), 500