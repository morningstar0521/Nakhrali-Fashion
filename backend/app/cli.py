import click
from flask.cli import with_appcontext
from app import db
from app.models import *

def register_commands(app):
    """Register CLI commands for the application"""
    
    @app.cli.command('init-db')
    @with_appcontext
    def init_db():
        """Initialize the database."""
        db.create_all()
        click.echo('Initialized the database.')
    
    @app.cli.command('seed-db')
    @with_appcontext
    def seed_db():
        """Seed the database with initial data."""
        # Create categories
        categories = [
            {'name': 'Rings', 'slug': 'rings', 'description': 'Beautiful rings for every occasion'},
            {'name': 'Earrings', 'slug': 'earrings', 'description': 'Elegant earrings collection'},
            {'name': 'Necklaces', 'slug': 'necklaces', 'description': 'Stunning necklaces'},
            {'name': 'Bangles', 'slug': 'bangles', 'description': 'Traditional bangles'},
            {'name': 'Bracelets', 'slug': 'bracelets', 'description': 'Modern bracelets'},
            {'name': 'Bridal', 'slug': 'bridal', 'description': 'Bridal jewelry collection'},
            {'name': 'Everyday', 'slug': 'everyday', 'description': 'Everyday jewelry'}
        ]
        
        for cat_data in categories:
            # Check if category already exists
            existing = Category.query.filter_by(name=cat_data['name']).first()
            if not existing:
                category = Category(**cat_data)
                db.session.add(category)
                click.echo(f"Added category: {cat_data['name']}")
            else:
                click.echo(f"Category already exists: {cat_data['name']}")
        
        # Create collections
        collections = [
            {'name': 'Festive Collection', 'slug': 'festive', 'description': 'Special festive jewelry'},
            {'name': 'Office Wear', 'slug': 'office-wear', 'description': 'Professional jewelry'},
            {'name': 'Gifting', 'slug': 'gifting', 'description': 'Perfect gifts for loved ones'}
        ]
        
        for col_data in collections:
            # Check if collection already exists
            existing = Collection.query.filter_by(name=col_data['name']).first()
            if not existing:
                collection = Collection(**col_data)
                db.session.add(collection)
                click.echo(f"Added collection: {col_data['name']}")
            else:
                click.echo(f"Collection already exists: {col_data['name']}")
        
        try:
            db.session.commit()
            click.echo('Database seeded successfully.')
        except Exception as e:
            db.session.rollback()
            click.echo(f'Error seeding database: {str(e)}')
    
    @app.cli.command('create-admin')
    @click.argument('email')
    @click.argument('password')
    @with_appcontext
    def create_admin(email, password):
        """Create an admin user."""
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            click.echo(f'User {email} already exists.')
            return
        
        user = User(
            email=email,
            password=password,
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        user.is_verified = True
        db.session.add(user)
        db.session.commit()
        click.echo(f'Admin user {email} created successfully.') 