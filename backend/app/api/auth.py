from flask import Blueprint, request, jsonify, current_app, url_for, redirect, session
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from app import db, limiter
from app.models.user import User, UserProfile
from app.utils.validators import validate_email, validate_password, validate_phone
from app.utils.decorators import admin_required
import uuid
from datetime import datetime, timedelta
import requests
import json
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate email
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password
        if not validate_password(data['password']):
            return jsonify({'error': 'Password must be at least 8 characters long'}), 400
        
        # Check if user with this email already exists
        existing_user = User.query.filter_by(email=data['email'].lower()).first()
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 409
        
        # Validate phone if provided
        phone = data.get('phone')
        if phone and not validate_phone(phone):
            return jsonify({'error': 'Invalid phone number format'}), 400
            
        # Check if user with this phone number already exists
        if phone:
            existing_phone = User.query.filter_by(phone=phone).first()
            if existing_phone:
                return jsonify({'error': 'User with this phone number already exists'}), 409
        
        # Create new user
        user = User(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=phone
        )
        
        db.session.add(user)
        db.session.flush()  # Get user ID before committing
        
        # Create user profile with additional data
        profile_data = {
            'user_id': user.id
        }
        
        # Add optional profile fields
        if data.get('date_of_birth'):
            try:
                profile_data['date_of_birth'] = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
            except ValueError:
                pass
        
        if data.get('gender'):
            profile_data['gender'] = data['gender']
        
        # Handle preferences
        preferences = {}
        if data.get('preferred_styles'):
            preferences['jewelry_styles'] = data['preferred_styles']
        if data.get('newsletter_subscription') is not None:
            preferences['newsletter'] = data['newsletter_subscription']
        
        if preferences:
            profile_data['preferences'] = preferences
        
        profile = UserProfile(**profile_data)
        
        db.session.add(profile)
        db.session.commit()
        
        # Create access and refresh tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user by email
        user = User.query.filter_by(email=data['email'].lower()).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 403
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Create tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    try:
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'access_token': new_access_token
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Token refresh error: {str(e)}")
        return jsonify({'error': 'Token refresh failed'}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """User logout endpoint"""
    try:
        # In a real application, you might want to blacklist the token
        # For now, we'll just return a success message
        return jsonify({'message': 'Logout successful'}), 200
        
    except Exception as e:
        current_app.logger.error(f"Logout error: {str(e)}")
        return jsonify({'error': 'Logout failed'}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user.to_dict(),
            'profile': user.profile.to_dict() if user.profile else None
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get profile error: {str(e)}")
        return jsonify({'error': 'Failed to get profile'}), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update current user profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update basic user info
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'phone' in data:
            if not validate_phone(data['phone']):
                return jsonify({'error': 'Invalid phone number format'}), 400
            user.phone = data['phone']
        
        # Update profile info
        if user.profile:
            if 'date_of_birth' in data:
                user.profile.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
            if 'gender' in data:
                user.profile.gender = data['gender']
            if 'preferences' in data:
                user.profile.preferences = data['preferences']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict(),
            'profile': user.profile.to_dict() if user.profile else None
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Update profile error: {str(e)}")
        return jsonify({'error': 'Failed to update profile'}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        if not data.get('current_password') or not data.get('new_password'):
            return jsonify({'error': 'Current password and new password are required'}), 400
        
        # Verify current password
        if not user.check_password(data['current_password']):
            return jsonify({'error': 'Current password is incorrect'}), 401
        
        # Validate new password
        if not validate_password(data['new_password']):
            return jsonify({'error': 'New password must be at least 8 characters long'}), 400
        
        # Update password
        user.password_hash = user._hash_password(data['new_password'])
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Change password error: {str(e)}")
        return jsonify({'error': 'Failed to change password'}), 500

@auth_bp.route('/forgot-password', methods=['POST'])
@limiter.limit("3 per hour")
def forgot_password():
    """Send password reset email"""
    try:
        data = request.get_json()
        
        if not data.get('email'):
            return jsonify({'error': 'Email is required'}), 400
        
        user = User.query.filter_by(email=data['email'].lower()).first()
        
        if not user:
            # Don't reveal if user exists or not for security
            return jsonify({'message': 'If the email exists, a reset link has been sent'}), 200
        
        # Generate reset token (in a real app, you'd send this via email)
        reset_token = str(uuid.uuid4())
        # Store reset token in database or cache with expiration
        
        return jsonify({
            'message': 'If the email exists, a reset link has been sent',
            'reset_token': reset_token  # Remove this in production
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Forgot password error: {str(e)}")
        return jsonify({'error': 'Failed to process request'}), 500

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset password with token"""
    try:
        data = request.get_json()
        
        if not data.get('token') or not data.get('new_password'):
            return jsonify({'error': 'Token and new password are required'}), 400
        
        # Validate token and get user (implement token validation)
        # For now, we'll just return a success message
        
        return jsonify({'message': 'Password reset successfully'}), 200
        
    except Exception as e:
        current_app.logger.error(f"Reset password error: {str(e)}")
        return jsonify({'error': 'Failed to reset password'}), 500

@auth_bp.route('/verify-email', methods=['POST'])
@jwt_required()
def verify_email():
    """Verify user email"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if user.is_verified:
            return jsonify({'message': 'Email already verified'}), 200
        
        # In a real app, you'd send verification email
        # For now, we'll just mark as verified
        user.is_verified = True
        user.email_verified_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Email verified successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Email verification error: {str(e)}")
        return jsonify({'error': 'Failed to verify email'}), 500

@auth_bp.route('/google/auth', methods=['GET'])
def google_auth():
    """Initiate Google OAuth flow"""
    try:
        # Google OAuth configuration
        client_id = os.environ.get('GOOGLE_CLIENT_ID')
        redirect_uri = os.environ.get('GOOGLE_REDIRECT_URI')
        
        if not client_id or not redirect_uri:
            current_app.logger.error("Google OAuth credentials not configured")
            return jsonify({'error': 'Google authentication is not available'}), 500
        
        # Google OAuth authorization URL
        auth_url = 'https://accounts.google.com/o/oauth2/auth'
        scope = 'email profile'
        
        # Generate state token to prevent CSRF
        state = str(uuid.uuid4())
        session['oauth_state'] = state
        
        # Build authorization URL
        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': scope,
            'state': state,
            'access_type': 'offline',
            'prompt': 'select_account'
        }
        
        auth_url = f"{auth_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
        
        return jsonify({'auth_url': auth_url}), 200
        
    except Exception as e:
        current_app.logger.error(f"Google auth initiation error: {str(e)}")
        return jsonify({'error': 'Failed to initiate Google authentication'}), 500

@auth_bp.route('/google/callback', methods=['POST'])
def google_callback():
    """Handle Google OAuth callback"""
    try:
        data = request.get_json()
        auth_code = data.get('code')
        state = data.get('state')
        
        if not auth_code:
            return jsonify({'error': 'Authorization code is required'}), 400
        
        # Verify state to prevent CSRF
        if 'oauth_state' not in session or session['oauth_state'] != state:
            return jsonify({'error': 'Invalid state parameter'}), 400
        
        # Google OAuth configuration
        client_id = os.environ.get('GOOGLE_CLIENT_ID')
        client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
        redirect_uri = os.environ.get('GOOGLE_REDIRECT_URI')
        
        if not client_id or not client_secret or not redirect_uri:
            return jsonify({'error': 'Google authentication is not available'}), 500
        
        # Exchange authorization code for access token
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'code': auth_code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }
        
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()
        
        if 'access_token' not in token_json:
            return jsonify({'error': 'Failed to obtain access token'}), 400
        
        # Get user info from Google
        userinfo_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        headers = {'Authorization': f"Bearer {token_json['access_token']}"}
        userinfo_response = requests.get(userinfo_url, headers=headers)
        userinfo = userinfo_response.json()
        
        if 'email' not in userinfo:
            return jsonify({'error': 'Failed to get user info from Google'}), 400
        
        # Check if user exists
        user = User.query.filter_by(email=userinfo['email'].lower()).first()
        
        if user:
            # User exists
            if not user.google_id:
                # User exists but doesn't have Google ID, link account
                user.google_id = userinfo.get('sub') # Google's unique user ID
                user.is_verified = True # Google already verified the email
                db.session.commit()
            # If user exists and has google_id, proceed to login

        else:
            # Create new user
            user = User(
                email=userinfo['email'],
                password=str(uuid.uuid4()),  # Generate random password
                first_name=userinfo.get('given_name', ''),
                last_name=userinfo.get('family_name', ''),
                google_id=userinfo.get('sub'), # Store Google's unique user ID
                is_verified=True # Google already verified the email
            )
            db.session.add(user)
            db.session.flush()  # Get user ID before committing
            # Create user profile
            profile_data = {
                'user_id': user.id,
                'profile_picture': userinfo.get('picture')
            }
            profile = UserProfile(**profile_data)
            db.session.add(profile)
            db.session.commit()
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Create tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Google authentication successful',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Google callback error: {str(e)}")
        return jsonify({'error': 'Google authentication failed'}), 500