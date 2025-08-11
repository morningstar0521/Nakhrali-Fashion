# Nakhrali Fashion - Complete Deployment Guide

This guide will help you deploy the Nakhrali Fashion e-commerce application to production with global hosting.

## 🏗️ Architecture Overview

- **Frontend**: Vue.js 3 + Nuxt.js 3 (SSR, SEO-optimized)
- **Backend**: Flask + PostgreSQL + Redis
- **Database**: PostgreSQL (cloud-hosted)
- **File Storage**: AWS S3
- **Payment**: Stripe + Razorpay
- **Hosting**: Vercel/Netlify (Frontend) + Render/Railway (Backend)

## 📋 Prerequisites

1. **GitHub Account** - for code repository
2. **Vercel Account** - for frontend hosting
3. **Render Account** - for backend hosting
4. **Supabase/Neon Account** - for PostgreSQL database
5. **AWS Account** - for S3 file storage
6. **Stripe Account** - for payment processing

## 🚀 Step-by-Step Deployment

### 1. Database Setup (Supabase/Neon)

#### Option A: Supabase (Recommended)
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Go to Settings → Database
4. Copy the connection string
5. Note down the database URL for later use

#### Option B: Neon (Alternative)
1. Go to [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string
4. Note down the database URL for later use

### 2. Backend Deployment (Render)

1. **Fork/Clone the Repository**
   ```bash
   git clone https://github.com/your-username/nakhrali-fashion.git
   cd nakhrali-fashion
   ```

2. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

3. **Deploy Backend Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - **Name**: `nakhrali-fashion-backend`
     - **Root Directory**: `backend`
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn run:app --bind 0.0.0.0:$PORT --workers 4`

4. **Set Environment Variables**
   ```
   DATABASE_URL=your-supabase-neon-connection-string
   SECRET_KEY=your-super-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   CORS_ORIGINS=https://your-frontend-domain.vercel.app
   AWS_ACCESS_KEY_ID=your-aws-access-key
   AWS_SECRET_ACCESS_KEY=your-aws-secret-key
   S3_BUCKET=your-s3-bucket-name
   STRIPE_SECRET_KEY=your-stripe-secret-key
   RAZORPAY_KEY_ID=your-razorpay-key-id
   RAZORPAY_KEY_SECRET=your-razorpay-secret-key
   REDIS_URL=your-redis-url
   ADMIN_EMAIL=admin@nakhrali.com
   ADMIN_PASSWORD=secure-admin-password
   ```

5. **Deploy and Get Backend URL**
   - Render will provide a URL like: `https://nakhrali-fashion-backend.onrender.com`

### 3. Frontend Deployment (Vercel)

1. **Create Vercel Account**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub

2. **Deploy Frontend**
   - Click "New Project"
   - Import your GitHub repository
   - Configure:
     - **Framework Preset**: Nuxt.js
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `.output/public`

3. **Set Environment Variables**
   ```
   API_BASE_URL=https://your-backend-url.onrender.com/api
   ```

4. **Deploy and Get Frontend URL**
   - Vercel will provide a URL like: `https://nakhrali-fashion.vercel.app`

### 4. AWS S3 Setup (File Storage)

1. **Create S3 Bucket**
   - Go to AWS Console → S3
   - Create a new bucket: `nakhrali-fashion-uploads`
   - Enable CORS for the bucket

2. **Create IAM User**
   - Go to IAM → Users → Create User
   - Attach policy: `AmazonS3FullAccess`
   - Generate access keys

3. **Update Environment Variables**
   - Add AWS credentials to your backend environment variables

### 5. Payment Gateway Setup

#### Stripe Setup
1. Go to [stripe.com](https://stripe.com)
2. Create account and get API keys
3. Add keys to backend environment variables

#### Razorpay Setup (for India)
1. Go to [razorpay.com](https://razorpay.com)
2. Create account and get API keys
3. Add keys to backend environment variables

### 6. Redis Setup (Optional)

For production caching and sessions:
1. Use Redis Cloud or Upstash
2. Get connection URL
3. Add to backend environment variables

## 🔧 Configuration Files

### Backend Environment (.env)
```bash
# Copy from backend/env.example
cp backend/env.example backend/.env
# Edit with your actual values
```

### Frontend Environment
```bash
# Create .env in frontend directory
echo "API_BASE_URL=https://your-backend-url.onrender.com/api" > frontend/.env
```

## 🧪 Testing Deployment

### 1. Test Backend API
```bash
curl -X GET https://your-backend-url.onrender.com/api/health
```

### 2. Test Frontend
- Visit your Vercel URL
- Try registering a new user
- Test login functionality

### 3. Test Database Connection
- Check if user registration works
- Verify data is stored in database

## 🔒 Security Checklist

- [ ] All secrets are in environment variables
- [ ] HTTPS is enabled
- [ ] CORS is properly configured
- [ ] Database connection is secure
- [ ] JWT tokens are properly configured
- [ ] File uploads are secured
- [ ] Rate limiting is enabled

## 📊 Monitoring

### Backend Monitoring (Render)
- View logs in Render dashboard
- Monitor performance metrics
- Set up alerts for errors

### Frontend Monitoring (Vercel)
- View analytics in Vercel dashboard
- Monitor Core Web Vitals
- Set up error tracking

## 🔄 CI/CD Pipeline

### Automatic Deployments
- Push to `main` branch triggers deployment
- Preview deployments for pull requests
- Automatic database migrations

### Manual Deployments
```bash
# Backend
git push origin main

# Frontend
vercel --prod
```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check DATABASE_URL format
   - Verify database is accessible
   - Check firewall settings

2. **CORS Errors**
   - Verify CORS_ORIGINS includes frontend URL
   - Check for trailing slashes

3. **Build Failures**
   - Check Node.js version compatibility
   - Verify all dependencies are installed
   - Check for TypeScript errors

4. **Environment Variables**
   - Ensure all required variables are set
   - Check for typos in variable names
   - Verify values are properly quoted

### Debug Commands

```bash
# Check backend logs
curl -X GET https://your-backend-url.onrender.com/api/health

# Test database connection
python backend/deploy.py

# Check frontend build
cd frontend && npm run build
```

## 📞 Support

For deployment issues:
1. Check the logs in your hosting platform
2. Verify environment variables
3. Test locally first
4. Check the troubleshooting section above

## 🎉 Success!

Once deployed, your application will be available at:
- **Frontend**: `https://your-app.vercel.app`
- **Backend API**: `https://your-backend.onrender.com`
- **Database**: Managed by Supabase/Neon
- **File Storage**: AWS S3

Your e-commerce application is now globally accessible and production-ready! 