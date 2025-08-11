import os
import sys

# Add the current directory to the path so we can import the app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try to import the required modules
try:
    from app import create_app, db
    from app.models.user import User
    
    # Create the app and push the context
    app = create_app()
    with app.app_context():
        
        
        # Check if the admin user exists
        admin_user = User.query.filter_by(email='admin@nakhrali.com').first()
        print('Admin user exists:', admin_user is not None)
        
        
        # If the admin user doesn't exist, create it
        if not admin_user:
            print('Creating admin user...')
            admin_user = User(
                email='admin@nakhrali.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()
            print('Admin user created successfully!')
            
except ImportError as e:
    print(f'Error importing modules: {e}')
    print('Please make sure all required packages are installed.')
    print('Try running: pip install -r requirements.txt')
    sys.exit(1)
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)