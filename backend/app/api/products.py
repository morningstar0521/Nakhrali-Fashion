from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, limiter
from app.models.product import Product, Category, Collection, ProductImage, ProductVariant
from app.models.review import Review
from app.utils.decorators import handle_errors, paginate_response, cache_response
from app.utils.validators import validate_uuid
from sqlalchemy import and_, or_, desc, asc
import math

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
@handle_errors
@paginate_response
@cache_response(timeout=300)
def get_products(page=1, per_page=20):
    """Get products with filtering and pagination"""
    try:
        # Get query parameters
        category_id = request.args.get('category_id')
        collection_id = request.args.get('collection_id')
        search = request.args.get('search')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        material = request.args.get('material')
        occasion = request.args.get('occasion')
        style = request.args.get('style')
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        featured_only = request.args.get('featured_only', type=bool)
        
        # Build query
        query = Product.query.filter(Product.is_active == True)
        
        # Apply filters
        if category_id:
            if not validate_uuid(category_id):
                return jsonify({'error': 'Invalid category ID'}), 400
            query = query.filter(Product.category_id == category_id)
        
        if collection_id:
            if not validate_uuid(collection_id):
                return jsonify({'error': 'Invalid collection ID'}), 400
            query = query.filter(Product.collection_id == collection_id)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term),
                    Product.short_description.ilike(search_term),
                    Product.tags.contains([search])
                )
            )
        
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        if material:
            query = query.filter(Product.material.ilike(f"%{material}%"))
        
        if occasion:
            query = query.filter(Product.occasion.ilike(f"%{occasion}%"))
        
        if style:
            query = query.filter(Product.style.ilike(f"%{style}%"))
        
        if featured_only:
            query = query.filter(Product.is_featured == True)
        
        # Apply sorting
        if sort_by in ['name', 'price', 'created_at', 'sort_order']:
            if sort_order == 'desc':
                query = query.order_by(desc(getattr(Product, sort_by)))
            else:
                query = query.order_by(asc(getattr(Product, sort_by)))
        else:
            query = query.order_by(desc(Product.created_at))
        
        # Paginate
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        products = pagination.items
        
        # Calculate total pages
        total_pages = math.ceil(pagination.total / per_page)
        
        # Get product images and variants
        product_data = []
        for product in products:
            product_dict = product.to_dict()
            
            # Add images
            images = product.images.order_by(ProductImage.sort_order).all()
            product_dict['images'] = [img.to_dict() for img in images]
            
            # Add variants
            variants = product.variants.filter(ProductVariant.is_active == True).all()
            product_dict['variants'] = [variant.to_dict() for variant in variants]
            
            # Add average rating
            reviews = product.reviews.filter(Review.is_approved == True).all()
            if reviews:
                avg_rating = sum(review.rating for review in reviews) / len(reviews)
                product_dict['average_rating'] = round(avg_rating, 1)
                product_dict['review_count'] = len(reviews)
            else:
                product_dict['average_rating'] = 0
                product_dict['review_count'] = 0
            
            product_data.append(product_dict)
        
        return jsonify({
            'products': product_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'total_pages': total_pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get products error: {str(e)}")
        return jsonify({'error': 'Failed to fetch products'}), 500

@products_bp.route('/<product_id>', methods=['GET'])
@handle_errors
@cache_response(timeout=300)
def get_product(product_id):
    """Get single product details"""
    try:
        if not validate_uuid(product_id):
            return jsonify({'error': 'Invalid product ID'}), 400
        
        product = Product.query.get(product_id)
        if not product or not product.is_active:
            return jsonify({'error': 'Product not found'}), 404
        
        # Get product data
        product_dict = product.to_dict()
        
        # Add images
        images = product.images.order_by(ProductImage.sort_order).all()
        product_dict['images'] = [img.to_dict() for img in images]
        
        # Add variants
        variants = product.variants.filter(ProductVariant.is_active == True).all()
        product_dict['variants'] = [variant.to_dict() for variant in variants]
        
        # Add reviews
        reviews = product.reviews.filter(Review.is_approved == True).order_by(desc(Review.created_at)).limit(10).all()
        product_dict['reviews'] = [review.to_dict() for review in reviews]
        
        # Add rating statistics
        all_reviews = product.reviews.filter(Review.is_approved == True).all()
        if all_reviews:
            ratings = [review.rating for review in all_reviews]
            product_dict['rating_stats'] = {
                'average_rating': round(sum(ratings) / len(ratings), 1),
                'total_reviews': len(ratings),
                'rating_distribution': {
                    '5': len([r for r in ratings if r == 5]),
                    '4': len([r for r in ratings if r == 4]),
                    '3': len([r for r in ratings if r == 3]),
                    '2': len([r for r in ratings if r == 2]),
                    '1': len([r for r in ratings if r == 1])
                }
            }
        else:
            product_dict['rating_stats'] = {
                'average_rating': 0,
                'total_reviews': 0,
                'rating_distribution': {'5': 0, '4': 0, '3': 0, '2': 0, '1': 0}
            }
        
        # Add related products
        related_products = Product.query.filter(
            and_(
                Product.is_active == True,
                Product.category_id == product.category_id,
                Product.id != product.id
            )
        ).limit(4).all()
        
        product_dict['related_products'] = [p.to_dict() for p in related_products]
        
        return jsonify({'product': product_dict}), 200
        
    except Exception as e:
        current_app.logger.error(f"Get product error: {str(e)}")
        return jsonify({'error': 'Failed to fetch product'}), 500

@products_bp.route('/categories', methods=['GET'])
@handle_errors
@cache_response(timeout=600)
def get_categories():
    """Get all product categories"""
    try:
        categories = Category.query.filter(Category.is_active == True).order_by(Category.sort_order).all()
        
        return jsonify({
            'categories': [category.to_dict() for category in categories]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get categories error: {str(e)}")
        return jsonify({'error': 'Failed to fetch categories'}), 500

@products_bp.route('/collections', methods=['GET'])
@handle_errors
@cache_response(timeout=600)
def get_collections():
    """Get all product collections"""
    try:
        collections = Collection.query.filter(Collection.is_active == True).all()
        
        return jsonify({
            'collections': [collection.to_dict() for collection in collections]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get collections error: {str(e)}")
        return jsonify({'error': 'Failed to fetch collections'}), 500

@products_bp.route('/featured', methods=['GET'])
@handle_errors
@cache_response(timeout=300)
def get_featured_products():
    """Get featured products"""
    try:
        featured_products = Product.query.filter(
            and_(
                Product.is_active == True,
                Product.is_featured == True
            )
        ).order_by(desc(Product.sort_order)).limit(8).all()
        
        product_data = []
        for product in featured_products:
            product_dict = product.to_dict()
            product_dict['main_image'] = product.get_main_image()
            product_data.append(product_dict)
        
        return jsonify({
            'featured_products': product_data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get featured products error: {str(e)}")
        return jsonify({'error': 'Failed to fetch featured products'}), 500

@products_bp.route('/search', methods=['GET'])
@handle_errors
@paginate_response
def search_products(page=1, per_page=20):
    """Search products with advanced filtering"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        # Build search query
        search_query = Product.query.filter(Product.is_active == True)
        
        # Split query into terms
        terms = query.split()
        conditions = []
        
        for term in terms:
            term_condition = or_(
                Product.name.ilike(f"%{term}%"),
                Product.description.ilike(f"%{term}%"),
                Product.short_description.ilike(f"%{term}%"),
                Product.material.ilike(f"%{term}%"),
                Product.occasion.ilike(f"%{term}%"),
                Product.style.ilike(f"%{term}%"),
                Product.tags.contains([term])
            )
            conditions.append(term_condition)
        
        if conditions:
            search_query = search_query.filter(and_(*conditions))
        
        # Apply additional filters
        category_id = request.args.get('category_id')
        if category_id and validate_uuid(category_id):
            search_query = search_query.filter(Product.category_id == category_id)
        
        min_price = request.args.get('min_price', type=float)
        if min_price is not None:
            search_query = search_query.filter(Product.price >= min_price)
        
        max_price = request.args.get('max_price', type=float)
        if max_price is not None:
            search_query = search_query.filter(Product.price <= max_price)
        
        # Sort by relevance (you could implement more sophisticated ranking)
        search_query = search_query.order_by(desc(Product.is_featured), desc(Product.created_at))
        
        # Paginate
        pagination = search_query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        products = pagination.items
        
        # Format response
        product_data = []
        for product in products:
            product_dict = product.to_dict()
            product_dict['main_image'] = product.get_main_image()
            product_data.append(product_dict)
        
        return jsonify({
            'products': product_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'total_pages': math.ceil(pagination.total / per_page),
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            },
            'search_query': query
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Search products error: {str(e)}")
        return jsonify({'error': 'Failed to search products'}), 500

@products_bp.route('/<product_id>/reviews', methods=['GET'])
@handle_errors
@paginate_response
def get_product_reviews(product_id, page=1, per_page=10):
    """Get product reviews"""
    try:
        if not validate_uuid(product_id):
            return jsonify({'error': 'Invalid product ID'}), 400
        
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        reviews = Review.query.filter(
            and_(
                Review.product_id == product_id,
                Review.is_approved == True
            )
        ).order_by(desc(Review.created_at))
        
        pagination = reviews.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'reviews': [review.to_dict() for review in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'total_pages': math.ceil(pagination.total / per_page),
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get product reviews error: {str(e)}")
        return jsonify({'error': 'Failed to fetch reviews'}), 500 