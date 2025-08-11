# Nakhrali Fashion - Complete E-commerce Solution

A modern, production-ready e-commerce platform for ethnic jewelry with Vue.js frontend and Flask backend.

## 🏗️ Architecture

- **Frontend**: Vue.js 3 + Nuxt.js 3 (SSR, SEO-optimized)
- **Backend**: Flask + PostgreSQL + Redis
- **Database**: PostgreSQL (cloud-hosted)
- **File Storage**: AWS S3
- **Payment**: Stripe + Razorpay
- **Hosting**: Vercel/Netlify (Frontend) + Render/Railway (Backend)

## ✨ Features

### 🔐 Authentication & Security
- JWT-based authentication
- Role-based access control (User, Admin, SuperAdmin)
- Password encryption with bcrypt
- Email verification
- Password reset functionality
- Rate limiting and security headers

### 🛍️ E-commerce Features
- Product catalog with categories and collections
- Advanced search and filtering
- Shopping cart and wishlist
- Order management and tracking
- Payment integration (Stripe, Razorpay)
- Product reviews and ratings
- Inventory management

### 🎨 Modern UI/UX
- Responsive design for all devices
- Progressive Web App (PWA)
- Dark/Light mode
- Smooth animations and transitions
- Accessibility compliant
- SEO optimized

### 🚀 Performance & Scalability
- Server-side rendering (SSR)
- Image optimization
- Caching with Redis
- CDN integration
- Database optimization
- API rate limiting

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- PostgreSQL
- Redis (optional)

### 1. Clone Repository
```bash
git clone https://github.com/your-username/nakhrali-fashion.git
cd nakhrali-fashion
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your configuration

# Set up database
createdb nakhrali_fashion
flask db upgrade
flask seed-db
flask create-admin admin@nakhrali.com admin123

# Start backend server
python run.py
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
echo "API_BASE_URL=http://localhost:8000/api" > .env

# Start development server
npm run dev
```

### 4. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Admin Panel: http://localhost:3000/admin

## 🌐 Production Deployment

### Quick Deploy (Recommended)

1. **Database Setup**
   - Create Supabase account: https://supabase.com
   - Create new project and get connection string

2. **Backend Deployment (Render)**
   - Fork this repository
   - Connect to Render: https://render.com
   - Deploy as Web Service with environment variables

3. **Frontend Deployment (Vercel)**
   - Connect repository to Vercel: https://vercel.com
   - Deploy with environment variables

4. **File Storage (AWS S3)**
   - Create S3 bucket and IAM user
   - Configure environment variables

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

## 📁 Project Structure

```
nakhrali-fashion/
├── backend/                 # Flask backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # Database models
│   │   ├── utils/          # Utilities
│   │   └── config.py       # Configuration
│   ├── migrations/         # Database migrations
│   ├── requirements.txt    # Python dependencies
│   ├── run.py             # Application entry point
│   └── deploy.py          # Deployment script
├── frontend/               # Vue.js frontend
│   ├── components/         # Vue components
│   ├── pages/             # Nuxt pages
│   ├── composables/       # Vue composables
│   ├── middleware/        # Route middleware
│   ├── assets/            # Static assets
│   └── nuxt.config.ts     # Nuxt configuration
├── DEPLOYMENT.md          # Deployment guide
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://username:password@host:port/database

# Security
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# AWS S3
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
S3_BUCKET=your-bucket-name

# Payment Gateways
STRIPE_SECRET_KEY=your-stripe-secret
RAZORPAY_KEY_ID=your-razorpay-key
RAZORPAY_KEY_SECRET=your-razorpay-secret

# Redis (optional)
REDIS_URL=redis://username:password@host:port

# CORS
CORS_ORIGINS=https://your-frontend-domain.com
```

#### Frontend (.env)
```bash
API_BASE_URL=https://your-backend-url.com/api
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

### API Testing
```bash
# Health check
curl https://your-backend-url.com/api/health

# Test registration
curl -X POST https://your-backend-url.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","first_name":"Test","last_name":"User"}'
```

## 📊 API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `POST /api/auth/refresh` - Refresh token
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile

### Product Endpoints
- `GET /api/products` - Get all products
- `GET /api/products/<id>` - Get product by ID
- `GET /api/products/categories` - Get categories
- `GET /api/products/collections` - Get collections

### Cart Endpoints
- `GET /api/cart` - Get user cart
- `POST /api/cart/add` - Add item to cart
- `PUT /api/cart/update/<id>` - Update cart item
- `DELETE /api/cart/remove/<id>` - Remove from cart

### Order Endpoints
- `GET /api/orders` - Get user orders
- `POST /api/orders/create` - Create new order
- `GET /api/orders/<id>` - Get order details

## 🔒 Security Features

- JWT token authentication
- Password hashing with bcrypt
- Rate limiting on API endpoints
- CORS protection
- Input validation and sanitization
- SQL injection protection
- XSS protection
- CSRF protection

## 🚀 Performance Features

- Database query optimization
- Redis caching
- Image compression and optimization
- CDN integration
- Lazy loading
- Code splitting
- Service worker for offline support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Issues**: Create an issue on GitHub
- **Email**: support@nakhrali.com

## 🎉 Acknowledgments

- Vue.js team for the amazing framework
- Nuxt.js team for SSR capabilities
- Flask team for the Python web framework
- All contributors and supporters

---

**Made with ❤️ for Nakhrali Fashion** 