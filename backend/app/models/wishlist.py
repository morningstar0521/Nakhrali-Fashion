from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Wishlist(db.Model):
    """User wishlist model"""
    __tablename__ = 'wishlists'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), default='My Wishlist')
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('WishlistItem', backref='wishlist', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_total_items(self):
        """Get total number of items in wishlist"""
        return self.items.count()
    
    def get_total_value(self):
        """Get total value of wishlist items"""
        total = 0
        for item in self.items:
            if item.product and item.product.is_active:
                total += float(item.product.price)
        return total
    
    def to_dict(self):
        """Convert wishlist to dictionary"""
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'name': self.name,
            'is_public': self.is_public,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'total_items': self.get_total_items(),
            'total_value': self.get_total_value()
        }

class WishlistItem(db.Model):
    """Individual items in wishlist"""
    __tablename__ = 'wishlist_items'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wishlist_id = db.Column(UUID(as_uuid=True), db.ForeignKey('wishlists.id'), nullable=False)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('products.id'), nullable=False)
    product_variant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product_variants.id'), nullable=True)
    
    # Item metadata
    notes = db.Column(db.Text, nullable=True)  # User notes about the item
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    product = db.relationship('Product')
    product_variant = db.relationship('ProductVariant')
    
    def to_dict(self):
        """Convert wishlist item to dictionary"""
        return {
            'id': str(self.id),
            'wishlist_id': str(self.wishlist_id),
            'product_id': str(self.product_id),
            'product_variant_id': str(self.product_variant_id) if self.product_variant_id else None,
            'notes': self.notes,
            'priority': self.priority,
            'added_at': self.added_at.isoformat(),
            'product': self.product.to_dict() if self.product else None,
            'product_variant': self.product_variant.to_dict() if self.product_variant else None
        } 