from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Category(db.Model):
    """Product categories like Rings, Earrings, Necklaces, etc."""
    __tablename__ = 'categories'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy='dynamic')
    
    def to_dict(self):
        """Convert category to dictionary"""
        return {
            'id': str(self.id),
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'image': self.image,
            'is_active': self.is_active,
            'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Collection(db.Model):
    """Special collections like Festive, Bridal, Officewear"""
    __tablename__ = 'collections'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), nullable=True)
    banner_image = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='collection', lazy='dynamic')
    
    def to_dict(self):
        """Convert collection to dictionary"""
        return {
            'id': str(self.id),
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'image': self.image,
            'banner_image': self.banner_image,
            'is_active': self.is_active,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Product(db.Model):
    """Main product model for jewelry items"""
    __tablename__ = 'products'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)
    short_description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    compare_at_price = db.Column(db.Numeric(10, 2), nullable=True)
    cost_price = db.Column(db.Numeric(10, 2), nullable=True)
    sku = db.Column(db.String(100), unique=True, nullable=True)
    barcode = db.Column(db.String(100), unique=True, nullable=True)
    
    # Product details
    material = db.Column(db.String(100), nullable=True)  # Gold, Silver, Platinum, etc.
    weight = db.Column(db.Numeric(8, 3), nullable=True)  # in grams
    purity = db.Column(db.String(20), nullable=True)  # 18K, 22K, 925, etc.
    occasion = db.Column(db.String(100), nullable=True)  # Bridal, Casual, Party, etc.
    style = db.Column(db.String(100), nullable=True)  # Traditional, Modern, Fusion, etc.
    
    # Inventory
    stock_quantity = db.Column(db.Integer, default=0)
    low_stock_threshold = db.Column(db.Integer, default=5)
    track_quantity = db.Column(db.Boolean, default=True)
    allow_backorder = db.Column(db.Boolean, default=False)
    
    # SEO and visibility
    meta_title = db.Column(db.String(255), nullable=True)
    meta_description = db.Column(db.Text, nullable=True)
    tags = db.Column(db.JSON, default=[])  # Array of tags
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    
    # Relationships
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('categories.id'), nullable=False)
    collection_id = db.Column(UUID(as_uuid=True), db.ForeignKey('collections.id'), nullable=True)
    images = db.relationship('ProductImage', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    variants = db.relationship('ProductVariant', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='product', lazy='dynamic')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)
        if not self.slug:
            self.slug = self._generate_slug()
    
    def _generate_slug(self):
        """Generate URL-friendly slug from product name"""
        import re
        slug = re.sub(r'[^\w\s-]', '', self.name.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug
    
    def get_discount_percentage(self):
        """Calculate discount percentage"""
        if self.compare_at_price and self.compare_at_price > self.price:
            return round(((self.compare_at_price - self.price) / self.compare_at_price) * 100, 2)
        return 0
    
    def is_in_stock(self):
        """Check if product is in stock"""
        if not self.track_quantity:
            return True
        return self.stock_quantity > 0
    
    def is_low_stock(self):
        """Check if product is low in stock"""
        return self.stock_quantity <= self.low_stock_threshold
    
    def get_main_image(self):
        """Get the main product image"""
        main_image = self.images.filter_by(is_primary=True).first()
        if main_image:
            return main_image.image_url
        # Fallback to first image
        first_image = self.images.first()
        return first_image.image_url if first_image else None
    
    def to_dict(self):
        """Convert product to dictionary"""
        return {
            'id': str(self.id),
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'short_description': self.short_description,
            'price': float(self.price),
            'compare_at_price': float(self.compare_at_price) if self.compare_at_price else None,
            'cost_price': float(self.cost_price) if self.cost_price else None,
            'sku': self.sku,
            'barcode': self.barcode,
            'material': self.material,
            'weight': float(self.weight) if self.weight else None,
            'purity': self.purity,
            'occasion': self.occasion,
            'style': self.style,
            'stock_quantity': self.stock_quantity,
            'low_stock_threshold': self.low_stock_threshold,
            'track_quantity': self.track_quantity,
            'allow_backorder': self.allow_backorder,
            'meta_title': self.meta_title,
            'meta_description': self.meta_description,
            'tags': self.tags,
            'is_active': self.is_active,
            'is_featured': self.is_featured,
            'sort_order': self.sort_order,
            'category_id': str(self.category_id),
            'collection_id': str(self.collection_id) if self.collection_id else None,
            'discount_percentage': self.get_discount_percentage(),
            'is_in_stock': self.is_in_stock(),
            'is_low_stock': self.is_low_stock(),
            'main_image': self.get_main_image(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ProductImage(db.Model):
    """Product images with zoom support"""
    __tablename__ = 'product_images'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('products.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    alt_text = db.Column(db.String(255), nullable=True)
    is_primary = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert image to dictionary"""
        return {
            'id': str(self.id),
            'product_id': str(self.product_id),
            'image_url': self.image_url,
            'alt_text': self.alt_text,
            'is_primary': self.is_primary,
            'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat()
        }

class ProductVariant(db.Model):
    """Product variants like size, color, metal type"""
    __tablename__ = 'product_variants'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('products.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # e.g., "Size", "Color", "Metal"
    value = db.Column(db.String(100), nullable=False)  # e.g., "18", "Rose Gold", "Yellow Gold"
    price_adjustment = db.Column(db.Numeric(10, 2), default=0)  # Additional cost for this variant
    stock_quantity = db.Column(db.Integer, default=0)
    sku = db.Column(db.String(100), unique=True, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert variant to dictionary"""
        return {
            'id': str(self.id),
            'product_id': str(self.product_id),
            'name': self.name,
            'value': self.value,
            'price_adjustment': float(self.price_adjustment),
            'stock_quantity': self.stock_quantity,
            'sku': self.sku,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 