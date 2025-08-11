#!/bin/bash

# Nakhrali Fashion - Complete Deployment Script
# This script handles the complete deployment of the e-commerce application

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    local missing_commands=()
    
    # Check for required commands
    if ! command_exists node; then
        missing_commands+=("node")
    fi
    
    if ! command_exists npm; then
        missing_commands+=("npm")
    fi
    
    if ! command_exists python3; then
        missing_commands+=("python3")
    fi
    
    if ! command_exists pip3; then
        missing_commands+=("pip3")
    fi
    
    if ! command_exists git; then
        missing_commands+=("git")
    fi
    
    if [ ${#missing_commands[@]} -ne 0 ]; then
        print_error "Missing required commands: ${missing_commands[*]}"
        print_status "Please install the missing commands and try again."
        exit 1
    fi
    
    print_success "All prerequisites are installed"
}

# Function to setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd backend
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip3 install -r requirements.txt
    
    # Setup environment variables
    if [ ! -f ".env" ]; then
        print_status "Creating environment file..."
        cp env.example .env
        print_warning "Please edit backend/.env with your configuration"
    fi
    
    # Setup database
    print_status "Setting up database..."
    flask db upgrade
    flask seed-db
    flask create-admin admin@nakhrali.com admin123
    
    cd ..
    print_success "Backend setup completed"
}

# Function to setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    # Setup environment variables
    if [ ! -f ".env" ]; then
        print_status "Creating environment file..."
        echo "API_BASE_URL=http://localhost:8000/api" > .env
    fi
    
    cd ..
    print_success "Frontend setup completed"
}

# Function to start development servers
start_dev() {
    print_status "Starting development servers..."
    
    # Start backend in background
    cd backend
    source venv/bin/activate
    python run.py &
    BACKEND_PID=$!
    cd ..
    
    # Start frontend in background
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    cd ..
    
    print_success "Development servers started"
    print_status "Backend: http://localhost:8000"
    print_status "Frontend: http://localhost:3000"
    print_status "Press Ctrl+C to stop servers"
    
    # Wait for user to stop
    trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
    wait
}

# Function to build for production
build_production() {
    print_status "Building for production..."
    
    # Build backend
    cd backend
    source venv/bin/activate
    pip3 install -r requirements.txt
    cd ..
    
    # Build frontend
    cd frontend
    npm run build
    cd ..
    
    print_success "Production build completed"
}

# Function to run tests
run_tests() {
    print_status "Running tests..."
    
    # Backend tests
    cd backend
    source venv/bin/activate
    python -m pytest tests/ -v
    cd ..
    
    # Frontend tests (if available)
    cd frontend
    if npm run test --if-present; then
        print_success "Frontend tests passed"
    else
        print_warning "No frontend tests found"
    fi
    cd ..
    
    print_success "All tests completed"
}

# Function to deploy with Docker
deploy_docker() {
    print_status "Deploying with Docker..."
    
    if ! command_exists docker; then
        print_error "Docker is not installed"
        exit 1
    fi
    
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    
    # Build and start services
    docker-compose up -d --build
    
    print_success "Docker deployment completed"
    print_status "Services are running on:"
    print_status "  - Frontend: http://localhost:3000"
    print_status "  - Backend: http://localhost:8000"
    print_status "  - Database: localhost:5432"
    print_status "  - Redis: localhost:6379"
}

# Function to show help
show_help() {
    echo "Nakhrali Fashion - Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  setup       - Setup the complete development environment"
    echo "  dev         - Start development servers"
    echo "  build       - Build for production"
    echo "  test        - Run all tests"
    echo "  docker      - Deploy with Docker"
    echo "  clean       - Clean up temporary files"
    echo "  help        - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 setup    # Initial setup"
    echo "  $0 dev      # Start development"
    echo "  $0 docker   # Deploy with Docker"
}

# Function to clean up
clean_up() {
    print_status "Cleaning up..."
    
    # Remove node_modules
    rm -rf node_modules
    rm -rf frontend/node_modules
    
    # Remove Python cache
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete
    
    # Remove build artifacts
    rm -rf frontend/.output
    rm -rf frontend/.nuxt
    
    print_success "Cleanup completed"
}

# Main script logic
main() {
    case "${1:-help}" in
        "setup")
            check_prerequisites
            setup_backend
            setup_frontend
            print_success "Setup completed successfully!"
            print_status "Next steps:"
            print_status "1. Edit backend/.env with your configuration"
            print_status "2. Run '$0 dev' to start development servers"
            ;;
        "dev")
            start_dev
            ;;
        "build")
            build_production
            ;;
        "test")
            run_tests
            ;;
        "docker")
            deploy_docker
            ;;
        "clean")
            clean_up
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run main function with all arguments
main "$@" 