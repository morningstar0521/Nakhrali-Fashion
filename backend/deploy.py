#!/usr/bin/env python3
"""
Deployment script for Nakhrali Fashion Backend
Handles database setup, migrations, and production configuration
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        sys.exit(1)

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['DATABASE_URL', 'SECRET_KEY', 'JWT_SECRET_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your deployment environment")
        sys.exit(1)
    
    print("✅ Environment variables check passed")

def setup_database():
    """Setup database and run migrations"""
    print("🗄️ Setting up database...")
    
    # Run database migrations
    run_command("flask db upgrade", "Running database migrations")
    
    # Seed database with initial data
    run_command("flask seed-db", "Seeding database with initial data")
    
    # Create admin user if not exists
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@nakhrali.com')
    admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
    
    run_command(f"flask create-admin {admin_email} {admin_password}", "Creating admin user")

def main():
    """Main deployment function"""
    print("🚀 Starting Nakhrali Fashion Backend Deployment")
    print("=" * 50)
    
    # Check environment
    check_environment()
    
    # Setup database
    setup_database()
    
    print("✅ Deployment completed successfully!")
    print("🎉 Backend is ready to serve requests")

if __name__ == "__main__":
    main() 