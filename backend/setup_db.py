#!/usr/bin/env python3
"""
Database setup script for Nakhrali Fashion
This script will create the database and initialize it with sample data
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def setup_database():
    """Set up the PostgreSQL database"""
    
    # Check if PostgreSQL is installed
    if not run_command("which psql", "Checking PostgreSQL installation"):
        print("❌ PostgreSQL is not installed. Please install PostgreSQL first.")
        print("   On macOS: brew install postgresql")
        print("   On Ubuntu: sudo apt-get install postgresql postgresql-contrib")
        return False
    
    # Create database
    db_name = "nakhrali_fashion"
    if not run_command(f"createdb {db_name}", f"Creating database '{db_name}'"):
        print(f"⚠️  Database '{db_name}' might already exist, continuing...")
    
    # Set up environment variables
    os.environ['FLASK_APP'] = 'run.py'
    os.environ['FLASK_ENV'] = 'development'
    os.environ['DATABASE_URL'] = f'postgresql://localhost/{db_name}'
    
    # Initialize Flask-Migrate
    if not run_command("flask db init", "Initializing database migrations"):
        print("⚠️  Migrations might already be initialized, continuing...")
    
    # Create initial migration
    if not run_command("flask db migrate -m 'Initial migration'", "Creating initial migration"):
        print("⚠️  Migration might already exist, continuing...")
    
    # Apply migrations
    if not run_command("flask db upgrade", "Applying database migrations"):
        return False
    
    # Seed database with initial data
    if not run_command("flask seed-db", "Seeding database with initial data"):
        print("⚠️  Seeding might have failed, but continuing...")
    
    # Create admin user
    admin_email = "admin@nakhrali.com"
    admin_password = "admin123"
    if not run_command(f"flask create-admin {admin_email} {admin_password}", "Creating admin user"):
        print("⚠️  Admin user creation might have failed, but continuing...")
    
    print(f"\n🎉 Database setup completed!")
    print(f"📊 Database: {db_name}")
    print(f"👤 Admin user: {admin_email}")
    print(f"🔑 Admin password: {admin_password}")
    print(f"\n🚀 You can now start the backend server with: python run.py")
    
    return True

if __name__ == "__main__":
    print("🏗️  Setting up Nakhrali Fashion Database...")
    print("=" * 50)
    
    if setup_database():
        print("\n✅ Database setup completed successfully!")
    else:
        print("\n❌ Database setup failed!")
        sys.exit(1) 