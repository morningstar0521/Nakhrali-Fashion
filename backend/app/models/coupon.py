from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Coupon(db.Model):
    """Discount coupons and promotional codes"""
    __tablename__ = 'coupons'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Discount details
    discount_type = db.Column(db.String(20), default='percentage')  # percentage, fixed
    discount_value = db.Column(db.Numeric(10, 2), nullable=False)
    max_discount = db.Column(db.Numeric(10, 2), nullable=True)
    min_order_amount = db.Column(db.Numeric(10, 2), default=0)
    
    # Usage limits
    max_uses = db.Column(db.Integer, nullable=True)
    max_uses_per_user = db.Column(db.Integer, default=1)
    current_uses = db.Column(db.Integer, default=0)
    
    # Validity
    is_active = db.Column(db.Boolean, default=True)
    valid_from = db.Column(db.DateTime, nullable=True)
    valid_until = db.Column(db.DateTime, nullable=True)
    
    # Restrictions
    applicable_categories = db.Column(db.JSON, default=[])  # Category IDs
    applicable_products = db.Column(db.JSON, default=[])  # Product IDs
    excluded_products = db.Column(db.JSON, default=[])  # Product IDs
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def is_valid(self):
        """Check if coupon is valid"""
        now = datetime.utcnow()
        
        if not self.is_active:
            return False
        
        if self.valid_from and now < self.valid_from:
            return False
        
        if self.valid_until and now > self.valid_until:
            return False
        
        if self.max_uses and self.current_uses >= self.max_uses:
            return False
        
        return True
    
    def calculate_discount(self, order_amount):
        """Calculate discount amount for given order amount"""
        if order_amount < self.min_order_amount:
            return 0
        
        if self.discount_type == 'percentage':
            discount = (order_amount * self.discount_value) / 100
            if self.max_discount:
                discount = min(discount, self.max_discount)
        else:
            discount = self.discount_value
        
        return discount
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'discount_type': self.discount_type,
            'discount_value': float(self.discount_value),
            'max_discount': float(self.max_discount) if self.max_discount else None,
            'min_order_amount': float(self.min_order_amount),
            'max_uses': self.max_uses,
            'max_uses_per_user': self.max_uses_per_user,
            'current_uses': self.current_uses,
            'is_active': self.is_active,
            'valid_from': self.valid_from.isoformat() if self.valid_from else None,
            'valid_until': self.valid_until.isoformat() if self.valid_until else None,
            'applicable_categories': self.applicable_categories,
            'applicable_products': self.applicable_products,
            'excluded_products': self.excluded_products,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_valid': self.is_valid()
        }

class CouponUsage(db.Model):
    """Track coupon usage by users"""
    __tablename__ = 'coupon_usages'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    coupon_id = db.Column(UUID(as_uuid=True), db.ForeignKey('coupons.id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey('orders.id'), nullable=False)
    
    discount_amount = db.Column(db.Numeric(10, 2), nullable=False)
    used_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'coupon_id': str(self.coupon_id),
            'user_id': str(self.user_id),
            'order_id': str(self.order_id),
            'discount_amount': float(self.discount_amount),
            'used_at': self.used_at.isoformat()
        } 