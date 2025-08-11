import re
from email_validator import validate_email as validate_email_format, EmailNotValidError

def validate_email(email):
    """Validate email format"""
    # Simple regex pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password):
    """Validate password strength"""
    # Simple validation - just check minimum length
    return len(password) >= 8

def validate_phone(phone):
    """Validate phone number format (Indian format)"""
    # Remove spaces, dashes, and parentheses
    phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check if it's a valid Indian phone number
    # Indian numbers start with +91 or 91 or 0 or 6-9
    pattern = r'^(\+91|91|0)?[6-9]\d{9}$'
    return bool(re.match(pattern, phone))

def validate_uuid(uuid_string):
    """Validate UUID format"""
    import uuid
    try:
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False

def sanitize_string(text, max_length=None):
    """Sanitize string input"""
    if not text:
        return ""
    
    # Remove HTML tags
    import re
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Truncate if max_length is specified
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text.strip()

def validate_price(price):
    """Validate price format"""
    try:
        price = float(price)
        return price >= 0
    except (ValueError, TypeError):
        return False

def validate_quantity(quantity):
    """Validate quantity format"""
    try:
        quantity = int(quantity)
        return quantity > 0
    except (ValueError, TypeError):
        return False