from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class SupportTicket(db.Model):
    """Customer support tickets"""
    __tablename__ = 'support_tickets'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey('orders.id'), nullable=True)
    
    # Ticket details
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, urgent
    status = db.Column(db.String(20), default='open')  # open, in_progress, resolved, closed
    
    # Assignment
    assigned_to = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=True)
    assigned_at = db.Column(db.DateTime, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)
    closed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    messages = db.relationship('TicketMessage', backref='ticket', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        super(SupportTicket, self).__init__(**kwargs)
        if not self.ticket_number:
            self.ticket_number = self._generate_ticket_number()
    
    def _generate_ticket_number(self):
        """Generate unique ticket number"""
        import random
        import string
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"TKT{timestamp}{random_suffix}"
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'ticket_number': self.ticket_number,
            'user_id': str(self.user_id),
            'order_id': str(self.order_id) if self.order_id else None,
            'subject': self.subject,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'assigned_to': str(self.assigned_to) if self.assigned_to else None,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'closed_at': self.closed_at.isoformat() if self.closed_at else None
        }

class TicketMessage(db.Model):
    """Messages in support tickets"""
    __tablename__ = 'ticket_messages'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id = db.Column(UUID(as_uuid=True), db.ForeignKey('support_tickets.id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    
    # Message details
    message = db.Column(db.Text, nullable=False)
    is_internal = db.Column(db.Boolean, default=False)  # Internal note vs customer message
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'ticket_id': str(self.ticket_id),
            'user_id': str(self.user_id),
            'message': self.message,
            'is_internal': self.is_internal,
            'created_at': self.created_at.isoformat()
        } 