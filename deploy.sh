#!/bin/bash

# DTEAM Django CV Application Deployment Script
# This script automates the deployment process on DigitalOcean

set -e  # Exit on any error

echo "🚀 Starting DTEAM Django CV Application Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_status "Checking prerequisites..."

# Check if .env.production exists
if [ ! -f .env.production ]; then
    print_warning ".env.production file not found. Creating template..."
    cat > .env.production << EOF
DEBUG=False
SECRET_KEY=your-super-secret-key-change-this-in-production
DB_NAME=cv_database
DB_USER=cv_user
DB_PASSWORD=your-secure-database-password
DB_HOST=db
DB_PORT=5432
USE_SQLITE=False
REDIS_URL=redis://redis:6379/0
OPENAI_API_KEY=your-openai-api-key-if-using-translation
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,YOUR_DROPLET_IP
EOF
    print_warning "Please edit .env.production with your actual values before continuing."
    read -p "Press Enter to continue after editing .env.production..."
fi

print_status "Building and starting services..."

# Stop any existing containers
docker-compose -f docker-compose.prod.yml down

# Build and start services
docker-compose -f docker-compose.prod.yml up --build -d

print_status "Waiting for services to start..."

# Wait for database to be ready
sleep 30

# Check if services are running
if docker-compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    print_status "Services are running successfully!"
else
    print_error "Some services failed to start. Check logs with: docker-compose -f docker-compose.prod.yml logs"
    exit 1
fi

print_status "Running database migrations..."

# Run migrations
docker-compose -f docker-compose.prod.yml exec -T web python manage.py migrate

print_status "Collecting static files..."

# Collect static files
docker-compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput

print_status "Loading sample data..."

# Load sample data
docker-compose -f docker-compose.prod.yml exec -T web python manage.py loaddata main/fixtures/sample_cv.json

print_status "Checking application health..."

# Check if application is responding
sleep 10
if curl -f http://localhost > /dev/null 2>&1; then
    print_status "✅ Application is running successfully!"
else
    print_warning "Application might still be starting. Please wait a moment and check manually."
fi

print_status "Deployment completed successfully!"

echo ""
echo "🌐 Your application should now be accessible at:"
echo "   http://YOUR_DROPLET_IP"
echo ""
echo "📋 Useful commands:"
echo "   View logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "   Stop services: docker-compose -f docker-compose.prod.yml down"
echo "   Restart services: docker-compose -f docker-compose.prod.yml restart"
echo "   Create superuser: docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser"
echo ""
echo "🔧 Next steps:"
echo "   1. Configure your domain name (optional)"
echo "   2. Set up SSL certificate with Let's Encrypt"
echo "   3. Configure firewall rules"
echo "   4. Set up monitoring and backups"
echo ""
print_status "Deployment script completed!"
