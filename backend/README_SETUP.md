# Backend Setup Guide

## Prerequisites

1. **Python 3.8+** installed
2. **PostgreSQL** installed and running
3. **Redis** installed and running (optional, for caching)

## Quick Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Set up Environment Variables
Copy the example environment file:
```bash
cp config.env .env
# Edit .env with your actual values
```

### 3. Create Database
```bash
# Create PostgreSQL database
createdb nakhrali_fashion

# Or use the setup script
python setup_db.py
```

### 4. Initialize Database
```bash
# Set Flask app
export FLASK_APP=run.py

# Initialize migrations
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade

# Seed database with sample data
flask seed-db

# Create admin user
flask create-admin admin@nakhrali.com admin123
```

### 5. Start the Server
```bash
python run.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `POST /api/auth/refresh` - Refresh token
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile

### Products
- `GET /api/products` - Get all products
- `GET /api/products/<id>` - Get product by ID
- `GET /api/products/categories` - Get categories
- `GET /api/products/collections` - Get collections

### Cart
- `GET /api/cart` - Get user cart
- `POST /api/cart/add` - Add item to cart
- `PUT /api/cart/update/<id>` - Update cart item
- `DELETE /api/cart/remove/<id>` - Remove from cart

### Orders
- `GET /api/orders` - Get user orders
- `POST /api/orders/create` - Create new order
- `GET /api/orders/<id>` - Get order details

## Database Schema

The database includes the following main tables:
- `users` - User accounts and profiles
- `products` - Product catalog
- `categories` - Product categories
- `collections` - Product collections
- `orders` - Customer orders
- `cart_items` - Shopping cart items
- `wishlist_items` - User wishlists
- `payments` - Payment transactions
- `reviews` - Product reviews

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Database Migrations
```bash
# Create new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade
```

### CLI Commands
```bash
# Create admin user
flask create-admin <email> <password>

# Seed database
flask seed-db

# Initialize database
flask init-db
```

## Troubleshooting

### Database Connection Issues
1. Make sure PostgreSQL is running
2. Check database exists: `psql -l`
3. Verify connection string in `.env`

### Migration Issues
1. Delete `migrations/` folder
2. Run `flask db init` again
3. Create new migration

### Import Errors
1. Make sure you're in the backend directory
2. Check virtual environment is activated
3. Install missing dependencies: `pip install -r requirements.txt` 