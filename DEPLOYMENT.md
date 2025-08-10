# Deployment Guide - DigitalOcean

This guide will help you deploy the DTEAM Django CV application to DigitalOcean using Docker and Docker Compose.

## Prerequisites

1. **DigitalOcean Account**: Create an account at [DigitalOcean](https://m.do.co/c/967939ea1e74) (get $200 credit with this referral link)
2. **Domain Name** (optional but recommended)
3. **SSH Key** for secure server access

## Step 1: Create a DigitalOcean Droplet

### 1.1 Create a New Droplet
1. Log in to your DigitalOcean account
2. Click "Create" → "Droplets"
3. Choose the following settings:
   - **Distribution**: Ubuntu 22.04 LTS
   - **Plan**: Basic (Choose based on your needs)
     - **Regular with SSD**: $6/month (1GB RAM, 1 vCPU, 25GB SSD)
     - **Regular with SSD**: $12/month (2GB RAM, 1 vCPU, 50GB SSD) - **Recommended**
   - **Datacenter Region**: Choose closest to your users
   - **Authentication**: SSH Key (recommended) or Password
   - **Hostname**: `dteam-cv-app` (or your preferred name)

### 1.2 Add SSH Key (Recommended)
1. Generate SSH key on your local machine:
   ```bash
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   ```
2. Copy your public key:
   ```bash
   cat ~/.ssh/id_rsa.pub
   ```
3. Add the key to DigitalOcean:
   - Go to Settings → Security → SSH Keys
   - Click "Add SSH Key"
   - Paste your public key and give it a name

## Step 2: Connect to Your Droplet

```bash
ssh root@YOUR_DROPLET_IP
```

Replace `YOUR_DROPLET_IP` with your actual droplet IP address.

## Step 3: Server Setup

### 3.1 Update System
```bash
apt update && apt upgrade -y
```

### 3.2 Install Docker and Docker Compose
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Add current user to docker group
usermod -aG docker $USER

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### 3.3 Install Additional Tools
```bash
# Install Git
apt install git -y

# Install Nginx (for reverse proxy)
apt install nginx -y

# Install Certbot (for SSL certificates)
apt install certbot python3-certbot-nginx -y
```

## Step 4: Deploy the Application

### 4.1 Clone the Repository
```bash
# Create application directory
mkdir -p /opt/dteam-cv-app
cd /opt/dteam-cv-app

# Clone your repository (replace with your actual repository URL)
git clone https://github.com/YOUR_USERNAME/DTEAM-django-practical-test.git .
```

### 4.2 Create Environment File
```bash
# Create production environment file
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
```

### 4.3 Create Production Docker Compose File
```bash
# Create production docker-compose file
cat > docker-compose.prod.yml << 'EOF'
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    restart: unless-stopped
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    networks:
      - app-network

  web:
    build: .
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn CVProject.wsgi:application --bind 0.0.0.0:8000 --workers 3"
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    env_file:
      - .env.production
    environment:
      - DB_HOST=db
      - USE_SQLITE=False
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    restart: unless-stopped
    networks:
      - app-network

  celery:
    build: .
    command: celery -A CVProject worker --loglevel=info
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    env_file:
      - .env.production
    environment:
      - DB_HOST=db
      - USE_SQLITE=False
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    restart: unless-stopped
    networks:
      - app-network

  celery-beat:
    build: .
    command: celery -A CVProject beat --loglevel=info
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    env_file:
      - .env.production
    environment:
      - DB_HOST=db
      - USE_SQLITE=False
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    restart: unless-stopped
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/app/staticfiles
      - media_volume:/app/media
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - web
    restart: unless-stopped
    networks:
      - app-network

volumes:
  postgres_data:
  static_volume:
  media_volume:

networks:
  app-network:
    driver: bridge
EOF
```

### 4.4 Create Nginx Configuration
```bash
# Create Nginx configuration
cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private must-revalidate auth;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    upstream django {
        server web:8000;
    }

    server {
        listen 80;
        server_name your-domain.com www.your-domain.com YOUR_DROPLET_IP;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

        # Static files
        location /static/ {
            alias /app/staticfiles/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Media files
        location /media/ {
            alias /app/media/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # API rate limiting
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Main application
        location / {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_redirect off;
        }
    }
}
EOF
```

### 4.5 Update Dockerfile for Production
```bash
# Update Dockerfile for production
cat > Dockerfile << 'EOF'
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
        gettext \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy project
COPY . .

# Create a non-root user
RUN adduser --disabled-password --gecos '' django

# Change ownership of the app directory
RUN chown -R django:django /app
USER django

# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "CVProject.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
EOF
```

### 4.6 Update Django Settings for Production
```bash
# Create production settings file
cat > CVProject/settings_production.py << 'EOF'
import os
from decouple import config
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

if config('USE_SQLITE', default=False, cast=bool):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS settings (uncomment when SSL is configured)
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# Celery Configuration
CELERY_BROKER_URL = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/app/django.log',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
EOF
```

### 4.7 Update WSGI Configuration
```bash
# Update wsgi.py to use production settings
cat > CVProject/wsgi.py << 'EOF'
import os
from decouple import config
from django.core.wsgi import get_wsgi_application

# Use production settings if in production environment
if config('DEBUG', default=True, cast=bool) == False:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CVProject.settings_production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CVProject.settings')

application = get_wsgi_application()
EOF
```

## Step 5: Deploy the Application

### 5.1 Build and Start Services
```bash
# Build and start the application
docker-compose -f docker-compose.prod.yml up --build -d

# Check if services are running
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### 5.2 Create Superuser (Optional)
```bash
# Create a superuser for admin access
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

### 5.3 Load Sample Data
```bash
# Load sample CV data
docker-compose -f docker-compose.prod.yml exec web python manage.py loaddata main/fixtures/sample_cv.json
```

## Step 6: Configure Domain and SSL (Optional)

### 6.1 Point Domain to Your Droplet
1. Go to your domain registrar
2. Update DNS A record to point to your droplet IP
3. Wait for DNS propagation (can take up to 48 hours)

### 6.2 Configure SSL Certificate
```bash
# Install SSL certificate with Let's Encrypt
certbot --nginx -d your-domain.com -d www.your-domain.com

# Test automatic renewal
certbot renew --dry-run
```

### 6.3 Update Nginx Configuration for SSL
```bash
# Update nginx.conf to include SSL configuration
# (This will be done automatically by certbot)
```

## Step 7: Monitoring and Maintenance

### 7.1 View Application Logs
```bash
# View web application logs
docker-compose -f docker-compose.prod.yml logs web

# View database logs
docker-compose -f docker-compose.prod.yml logs db

# View Celery logs
docker-compose -f docker-compose.prod.yml logs celery
```

### 7.2 Backup Database
```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U cv_user cv_database > backup_$DATE.sql
gzip backup_$DATE.sql
echo "Backup created: backup_$DATE.sql.gz"
EOF

chmod +x backup.sh
```

### 7.3 Update Application
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart services
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up --build -d

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

## Step 8: Security Considerations

### 8.1 Firewall Configuration
```bash
# Configure UFW firewall
ufw allow ssh
ufw allow 80
ufw allow 443
ufw enable
```

### 8.2 Regular Security Updates
```bash
# Update system packages regularly
apt update && apt upgrade -y

# Update Docker images
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

## Troubleshooting

### Common Issues

1. **Application not accessible**
   ```bash
   # Check if containers are running
   docker-compose -f docker-compose.prod.yml ps
   
   # Check logs
   docker-compose -f docker-compose.prod.yml logs web
   ```

2. **Database connection issues**
   ```bash
   # Check database logs
   docker-compose -f docker-compose.prod.yml logs db
   
   # Test database connection
   docker-compose -f docker-compose.prod.yml exec web python manage.py dbshell
   ```

3. **Static files not loading**
   ```bash
   # Collect static files
   docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
   ```

## Performance Optimization

### 8.1 Enable Caching
```bash
# Add Redis caching to Django settings
# Update settings_production.py with cache configuration
```

### 8.2 Database Optimization
```bash
# Run database optimization
docker-compose -f docker-compose.prod.yml exec web python manage.py dbshell
```

## Cost Optimization

1. **Choose appropriate droplet size** based on your needs
2. **Use volume snapshots** for backups instead of larger storage
3. **Monitor usage** through DigitalOcean dashboard
4. **Consider reserved instances** for long-term projects

## Support

If you encounter issues:
1. Check the logs: `docker-compose -f docker-compose.prod.yml logs`
2. Verify environment variables: `docker-compose -f docker-compose.prod.yml config`
3. Test individual services: `docker-compose -f docker-compose.prod.yml exec web python manage.py check`

Your application should now be accessible at:
- **HTTP**: http://YOUR_DROPLET_IP
- **HTTPS**: https://your-domain.com (after SSL configuration)
