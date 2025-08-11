from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Cart(db.Model):
    """Shopping cart model"""
    __tablename__ = 'carts'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.String(255), nullable=True, index=True)  # For guest users
    
    # Cart totals (calculated)
    subtotal = db.Column(db.Numeric(10, 2), default=0)
    tax_amount = db.Column(db.Numeric(10, 2), default=0)
    shipping_amount = db.Column(db.Numeric(10, 2), default=0)
    discount_amount = db.Column(db.Numeric(10, 2), default=0)
    total_amount = db.Column(db.Numeric(10, 2), default=0)
    
    # Applied coupon
    coupon_code = db.Column(db.String(50), nullable=True)
    coupon_discount = db.Column(db.Numeric(10, 2), default=0)
    
    # Cart metadata
    is_active = db.Column(db.Boolean, default=True)
    expires_at = db.Column(db.DateTime, nullable=True)  # Cart expiration
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('CartItem', backref='cart', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        super(Cart, self).__init__(**kwargs)
        if not self.expires_at:
            from datetime import timedelta
            self.expires_at = datetime.utcnow() + timedelta(days=30)  # 30 days expiration
    
    def get_total_items(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items)
    
    def get_total_weight(self):
        """Get total weight of items in cart"""
        total_weight = 0
        for item in self.items:
            if item.product and item.product.weight:
                total_weight += float(item.product.weight) * item.quantity
        return total_weight
    
    def calculate_totals(self):
        """Calculate cart totals"""
        subtotal = sum(item.total_price for item in self.items)
        
        # Calculate tax (GST - 18% for jewelry)
        tax_rate = 0.18
        tax_amount = subtotal * tax_rate
        
        # Calculate shipping (free above ₹5000, else ₹200)
        shipping_amount = 0 if subtotal >= 5000 else 200
        
        # Apply coupon discount
        discount_amount = self.coupon_discount
        
        # Calculate total
        total_amount = subtotal + tax_amount + shipping_amount - discount_amount
        
        # Update cart totals
        self.subtotal = subtotal
        self.tax_amount = tax_amount
        self.shipping_amount = shipping_amount
        self.discount_amount = discount_amount
        self.total_amount = total_amount
        
        return {
            'subtotal': float(subtotal),
            'tax_amount': float(tax_amount),
            'shipping_amount': float(shipping_amount),
            'discount_amount': float(discount_amount),
            'total_amount': float(total_amount)
        }
    
    def is_expired(self):
        """Check if cart is expired"""
        return datetime.utcnow() > self.expires_at
    
    def clear(self):
        """Clear all items from cart"""
        for item in self.items:
            db.session.delete(item)
        self.coupon_code = None
        self.coupon_discount = 0
        self.calculate_totals()
    
    def to_dict(self):
        """Convert cart to dictionary"""
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'session_id': self.session_id,
            'subtotal': float(self.subtotal),
            'tax_amount': float(self.tax_amount),
            'shipping_amount': float(self.shipping_amount),
            'discount_amount': float(self.discount_amount),
            'total_amount': float(self.total_amount),
            'coupon_code': self.coupon_code,
            'coupon_discount': float(self.coupon_discount),
            'is_active': self.is_active,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'total_items': self.get_total_items(),
            'total_weight': self.get_total_weight(),
            'is_expired': self.is_expired()
        }

class CartItem(db.Model):
    """Individual items in shopping cart"""
    __tablename__ = 'cart_items'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id = db.Column(UUID(as_uuid=True), db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('products.id'), nullable=False)
    product_variant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product_variants.id'), nullable=True)
    
    # Item details
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Variant selection
    selected_variant_name = db.Column(db.String(100), nullable=True)  # e.g., "Size", "Color"
    selected_variant_value = db.Column(db.String(100), nullable=True)  # e.g., "18", "Rose Gold"
    
    # Item metadata
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = db.relationship('Product')
    product_variant = db.relationship('ProductVariant')
    
    def __init__(self, **kwargs):
        super(CartItem, self).__init__(**kwargs)
        if not self.total_price:
            self.calculate_total()
    
    def calculate_total(self):
        """Calculate total price for this item"""
        base_price = float(self.unit_price)
        
        # Add variant price adjustment if applicable
        if self.product_variant:
            base_price += float(self.product_variant.price_adjustment)
        
        self.total_price = base_price * self.quantity
    
    def update_quantity(self, quantity):
        """Update item quantity"""
        if quantity <= 0:
            return False
        
        # Check stock availability
        if self.product and self.product.track_quantity:
            available_stock = self.product.stock_quantity
            if self.product_variant:
                available_stock = self.product_variant.stock_quantity
            
            if quantity > available_stock and not self.product.allow_backorder:
                return False
        
        self.quantity = quantity
        self.calculate_total()
        self.updated_at = datetime.utcnow()
        return True
    
    def is_available(self):
        """Check if item is still available for purchase"""
        if not self.product or not self.product.is_active:
            return False
        
        if self.product.track_quantity:
            available_stock = self.product.stock_quantity
            if self.product_variant:
                available_stock = self.product_variant.stock_quantity
            
            if available_stock < self.quantity and not self.product.allow_backorder:
                return False
        
        return True
    
    def get_price_breakdown(self):
        """Get detailed price breakdown"""
        base_price = float(self.unit_price)
        variant_adjustment = 0
        
        if self.product_variant:
            variant_adjustment = float(self.product_variant.price_adjustment)
        
        return {
            'base_price': base_price,
            'variant_adjustment': variant_adjustment,
            'unit_price': base_price + variant_adjustment,
            'quantity': self.quantity,
            'total_price': float(self.total_price)
        }
    
    def to_dict(self):
        """Convert cart item to dictionary"""
        return {
            'id': str(self.id),
            'cart_id': str(self.cart_id),
            'product_id': str(self.product_id),
            'product_variant_id': str(self.product_variant_id) if self.product_variant_id else None,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'total_price': float(self.total_price),
            'selected_variant_name': self.selected_variant_name,
            'selected_variant_value': self.selected_variant_value,
            'added_at': self.added_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_available': self.is_available(),
            'price_breakdown': self.get_price_breakdown(),
            'product': self.product.to_dict() if self.product else None,
            'product_variant': self.product_variant.to_dict() if self.product_variant else None
        } 