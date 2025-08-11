from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class PaymentMethod(db.Model):
    """Available payment methods"""
    __tablename__ = 'payment_methods'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    processing_fee = db.Column(db.Numeric(5, 2), default=0)  # Percentage
    min_amount = db.Column(db.Numeric(10, 2), nullable=True)
    max_amount = db.Column(db.Numeric(10, 2), nullable=True)
    icon = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'is_active': self.is_active,
            'processing_fee': float(self.processing_fee),
            'min_amount': float(self.min_amount) if self.min_amount else None,
            'max_amount': float(self.max_amount) if self.max_amount else None,
            'icon': self.icon,
            'created_at': self.created_at.isoformat()
        }

class Payment(db.Model):
    """Payment transactions"""
    __tablename__ = 'payments'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey('orders.id'), nullable=True)
    
    # Payment details
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='INR')
    payment_method = db.Column(db.String(50), nullable=False)  # COD, Online, etc.
    gateway = db.Column(db.String(50), nullable=True)  # Razorpay, Stripe, etc.
    
    # Transaction details
    transaction_id = db.Column(db.String(100), unique=True, nullable=True)
    gateway_transaction_id = db.Column(db.String(100), nullable=True)
    payment_status = db.Column(db.String(20), default='pending')  # pending, success, failed, refunded
    
    # Gateway response
    gateway_response = db.Column(db.JSON, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    
    # Timestamps
    initiated_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'order_id': str(self.order_id) if self.order_id else None,
            'amount': float(self.amount),
            'currency': self.currency,
            'payment_method': self.payment_method,
            'gateway': self.gateway,
            'transaction_id': self.transaction_id,
            'gateway_transaction_id': self.gateway_transaction_id,
            'payment_status': self.payment_status,
            'gateway_response': self.gateway_response,
            'error_message': self.error_message,
            'initiated_at': self.initiated_at.isoformat(),
            'processed_at': self.processed_at.isoformat() if self.processed_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 