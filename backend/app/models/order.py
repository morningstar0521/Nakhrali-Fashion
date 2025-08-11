from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from enum import Enum

class OrderStatus(Enum):
    """Order status enumeration"""
    PLACED = 'placed'
    CONFIRMED = 'confirmed'
    PROCESSING = 'processing'
    PACKED = 'packed'
    SHIPPED = 'shipped'
    OUT_FOR_DELIVERY = 'out_for_delivery'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
    RETURNED = 'returned'
    REFUNDED = 'refunded'

class Order(db.Model):
    """Order model for customer purchases"""
    __tablename__ = 'orders'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    
    # Order details
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PLACED)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    tax_amount = db.Column(db.Numeric(10, 2), default=0)
    shipping_amount = db.Column(db.Numeric(10, 2), default=0)
    discount_amount = db.Column(db.Numeric(10, 2), default=0)
    coupon_code = db.Column(db.String(50), nullable=True)
    
    # Shipping information
    shipping_address_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user_addresses.id'), nullable=True)
    billing_address_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user_addresses.id'), nullable=True)
    shipping_method = db.Column(db.String(100), nullable=True)  # Standard, Express, etc.
    tracking_number = db.Column(db.String(100), nullable=True)
    estimated_delivery = db.Column(db.Date, nullable=True)
    
    # Payment information
    payment_method = db.Column(db.String(50), nullable=True)  # COD, Online, etc.
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, failed, refunded
    transaction_id = db.Column(db.String(100), nullable=True)
    
    # Notes and communication
    customer_notes = db.Column(db.Text, nullable=True)
    admin_notes = db.Column(db.Text, nullable=True)
    
    # Timestamps
    placed_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    shipped_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    cancelled_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='order', lazy='dynamic')
    
    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)
        if not self.order_number:
            self.order_number = self._generate_order_number()
    
    def _generate_order_number(self):
        """Generate unique order number"""
        import random
        import string
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"NK{timestamp}{random_suffix}"
    
    def get_status_display(self):
        """Get human-readable status"""
        status_map = {
            OrderStatus.PLACED: 'Order Placed',
            OrderStatus.CONFIRMED: 'Order Confirmed',
            OrderStatus.PROCESSING: 'Processing',
            OrderStatus.PACKED: 'Packed',
            OrderStatus.SHIPPED: 'Shipped',
            OrderStatus.OUT_FOR_DELIVERY: 'Out for Delivery',
            OrderStatus.DELIVERED: 'Delivered',
            OrderStatus.CANCELLED: 'Cancelled',
            OrderStatus.RETURNED: 'Returned',
            OrderStatus.REFUNDED: 'Refunded'
        }
        return status_map.get(self.status, self.status.value)
    
    def can_cancel(self):
        """Check if order can be cancelled"""
        return self.status in [OrderStatus.PLACED, OrderStatus.CONFIRMED]
    
    def can_return(self):
        """Check if order can be returned"""
        return self.status == OrderStatus.DELIVERED
    
    def get_total_items(self):
        """Get total number of items in order"""
        return sum(item.quantity for item in self.items)
    
    def to_dict(self):
        """Convert order to dictionary"""
        return {
            'id': str(self.id),
            'order_number': self.order_number,
            'user_id': str(self.user_id),
            'status': self.status.value,
            'status_display': self.get_status_display(),
            'total_amount': float(self.total_amount),
            'subtotal': float(self.subtotal),
            'tax_amount': float(self.tax_amount),
            'shipping_amount': float(self.shipping_amount),
            'discount_amount': float(self.discount_amount),
            'coupon_code': self.coupon_code,
            'shipping_address_id': str(self.shipping_address_id) if self.shipping_address_id else None,
            'billing_address_id': str(self.billing_address_id) if self.billing_address_id else None,
            'shipping_method': self.shipping_method,
            'tracking_number': self.tracking_number,
            'estimated_delivery': self.estimated_delivery.isoformat() if self.estimated_delivery else None,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'transaction_id': self.transaction_id,
            'customer_notes': self.customer_notes,
            'admin_notes': self.admin_notes,
            'placed_at': self.placed_at.isoformat(),
            'confirmed_at': self.confirmed_at.isoformat() if self.confirmed_at else None,
            'shipped_at': self.shipped_at.isoformat() if self.shipped_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'cancelled_at': self.cancelled_at.isoformat() if self.cancelled_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'total_items': self.get_total_items(),
            'can_cancel': self.can_cancel(),
            'can_return': self.can_return()
        }

class OrderItem(db.Model):
    """Individual items in an order"""
    __tablename__ = 'order_items'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('products.id'), nullable=False)
    product_variant_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product_variants.id'), nullable=True)
    
    # Item details
    product_name = db.Column(db.String(255), nullable=False)  # Snapshot of product name at time of order
    product_sku = db.Column(db.String(100), nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Product details snapshot
    material = db.Column(db.String(100), nullable=True)
    weight = db.Column(db.Numeric(8, 3), nullable=True)
    purity = db.Column(db.String(20), nullable=True)
    
    # Variant details
    variant_name = db.Column(db.String(100), nullable=True)  # e.g., "Size", "Color"
    variant_value = db.Column(db.String(100), nullable=True)  # e.g., "18", "Rose Gold"
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    product = db.relationship('Product')
    product_variant = db.relationship('ProductVariant')
    
    def to_dict(self):
        """Convert order item to dictionary"""
        return {
            'id': str(self.id),
            'order_id': str(self.order_id),
            'product_id': str(self.product_id),
            'product_variant_id': str(self.product_variant_id) if self.product_variant_id else None,
            'product_name': self.product_name,
            'product_sku': self.product_sku,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'total_price': float(self.total_price),
            'material': self.material,
            'weight': float(self.weight) if self.weight else None,
            'purity': self.purity,
            'variant_name': self.variant_name,
            'variant_value': self.variant_value,
            'created_at': self.created_at.isoformat()
        } 