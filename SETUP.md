# 🚀 Nakhrali Fashion - Setup Guide

This guide will help you set up the complete Nakhrali Fashion e-commerce platform with both backend and frontend.

## 📋 Prerequisites

Before starting, ensure you have the following installed:

- **Node.js** (v18 or higher)
- **Python** (v3.11 or higher)
- **PostgreSQL** (v14 or higher)
- **Redis** (v6 or higher)
- **Git**

## 🛠️ Backend Setup

### 1. Database Setup

```bash
# Create PostgreSQL database
createdb nakhrali_fashion
createdb nakhrali_fashion_test
```

### 2. Python Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the backend directory:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database
DATABASE_URL=postgresql://localhost/nakhrali_fashion

# Redis
REDIS_URL=redis://localhost:6379/0

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# AWS S3 (Optional)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1
S3_BUCKET=nakhrali-fashion

# Payment Gateways (Optional)
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-secret-key
```

### 4. Database Initialization

```bash
# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Seed database with initial data
flask seed-db

# Create admin user
flask create-admin admin@nakhrali.com password123
```

### 5. Run Backend

```bash
# Development server
flask run

# Or with gunicorn for production
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 🎨 Frontend Setup

### 1. Install Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### 2. Environment Variables

Create a `.env` file in the frontend directory:

```env
# API Configuration
API_BASE_URL=http://localhost:5000/api

# App Configuration
NUXT_PUBLIC_APP_NAME=Nakhrali Fashion
NUXT_PUBLIC_APP_DESCRIPTION=Where Elegance Meets Emotion
```

### 3. Run Frontend

```bash
# Development server
npm run dev

# Build for production
npm run build
npm run preview
```

## 🐳 Docker Setup (Optional)

### 1. Using Docker Compose

```bash
# Build and run all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 2. Individual Docker Commands

```bash
# Backend
docker build -t nakhrali-backend ./backend
docker run -p 5000:5000 nakhrali-backend

# Frontend
docker build -t nakhrali-frontend ./frontend
docker run -p 3000:3000 nakhrali-frontend
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
python -m pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## 📊 Monitoring & Analytics

### 1. Application Monitoring

- **Sentry**: Error tracking and performance monitoring
- **Logs**: Structured logging with correlation IDs
- **Health Checks**: `/health` endpoint for monitoring

### 2. Analytics Integration

- **Google Analytics 4**: User behavior tracking
- **Custom Events**: E-commerce specific tracking
- **Conversion Funnels**: Purchase flow analysis

## 🔒 Security Checklist

- [ ] HTTPS enabled in production
- [ ] CORS properly configured
- [ ] Rate limiting implemented
- [ ] Input validation on all endpoints
- [ ] SQL injection protection
- [ ] XSS protection
- [ ] CSRF protection
- [ ] Secure headers configured
- [ ] Environment variables secured
- [ ] Database credentials encrypted

## 🚀 Deployment

### 1. Backend Deployment

```bash
# Set production environment
export FLASK_ENV=production

# Run migrations
flask db upgrade

# Start with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### 2. Frontend Deployment

```bash
# Build for production
npm run build

# Deploy to Vercel/Netlify
# Or serve static files with nginx
```

### 3. Database Backup

```bash
# Create backup
pg_dump nakhrali_fashion > backup.sql

# Restore backup
psql nakhrali_fashion < backup.sql
```

## 📱 PWA Features

The frontend includes Progressive Web App features:

- **Service Worker**: Offline functionality
- **Manifest**: App-like experience
- **Push Notifications**: Order updates
- **Install Prompt**: Add to home screen

## 🔧 Development Tools

### 1. Code Quality

```bash
# Backend
pip install black flake8 mypy
black app/
flake8 app/
mypy app/

# Frontend
npm run lint
npm run format
```

### 2. Database Management

```bash
# View database
flask shell
# Then: db.engine.execute("SELECT * FROM users")

# Reset database
flask db downgrade base
flask db upgrade
```

## 📈 Performance Optimization

### 1. Backend

- **Redis Caching**: Session and data caching
- **Database Indexing**: Optimized queries
- **Image Optimization**: WebP format support
- **CDN Integration**: Static asset delivery

### 2. Frontend

- **Lazy Loading**: Images and components
- **Code Splitting**: Route-based splitting
- **Service Worker**: Caching strategies
- **Image Optimization**: Responsive images

## 🎯 Key Features Implemented

### ✅ Backend Features

- **Authentication System**: JWT-based auth with roles
- **Product Management**: CRUD with variants and images
- **Order Management**: Complete order lifecycle
- **Cart System**: Persistent cart with calculations
- **Payment Integration**: Razorpay/Stripe ready
- **User Management**: Profiles, addresses, preferences
- **Admin Panel**: Dashboard and management tools
- **API Documentation**: Comprehensive endpoints

### ✅ Frontend Features

- **Responsive Design**: Mobile-first approach
- **Luxury UI/UX**: Premium jewelry brand styling
- **Product Catalog**: Advanced filtering and search
- **Shopping Cart**: Real-time updates
- **User Dashboard**: Account management
- **PWA Support**: Offline functionality
- **SEO Optimized**: Meta tags and structured data

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Error**
   ```bash
   # Check PostgreSQL is running
   sudo systemctl status postgresql
   
   # Create database if missing
   createdb nakhrali_fashion
   ```

2. **Redis Connection Error**
   ```bash
   # Check Redis is running
   redis-cli ping
   
   # Start Redis if needed
   sudo systemctl start redis
   ```

3. **Frontend Build Errors**
   ```bash
   # Clear node modules
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **CORS Issues**
   ```bash
   # Check CORS configuration in backend
   # Ensure frontend URL is in CORS_ORIGINS
   ```

## 📞 Support

For technical support or questions:

- **Email**: support@nakhralifashion.com
- **Documentation**: `/docs` directory
- **Issues**: GitHub repository issues

## 🎉 Getting Started

1. Follow the setup guide above
2. Start with the backend API
3. Configure the frontend
4. Test the complete flow
5. Deploy to production

**Happy coding! 🚀** 