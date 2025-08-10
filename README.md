# DTEAM - Django Developer Practical Test

A comprehensive Django web application demonstrating full-stack development skills with modern technologies.

## 🚀 **Live Demo**
**Production URL**: https://dteam-django-practical-test-production.up.railway.app  
**Admin Access**: admin/admin123

## 📋 **Project Overview**

This project implements a CV management system with the following features:

- **CV Management**: Create, view, and manage professional CVs
- **PDF Generation**: Generate and download professional PDF CVs
- **REST API**: Full CRUD operations with Django REST Framework
- **Background Tasks**: Email notifications and PDF processing with Celery
- **AI Translation**: Multi-language CV translation using OpenAI
- **Request Logging**: Comprehensive request tracking and monitoring
- **Production Deployment**: Live deployment on Railway with PostgreSQL

## 🛠 **Technical Stack**

### **Backend**
- Django 5.2.5
- Django REST Framework
- PostgreSQL (production) / SQLite (development)
- Redis + Celery (background tasks)
- ReportLab (PDF generation)
- OpenAI API (translation service)

### **Frontend**
- Bootstrap 5 (responsive UI)
- Font Awesome (icons)
- JavaScript + AJAX (interactive features)

### **DevOps**
- Docker & Docker Compose
- Railway (cloud deployment)
- Gunicorn (production server)
- WhiteNoise (static files)

## 🎯 **Implemented Features**

### ✅ **All 9 Required Tasks Completed**

1. **Django Fundamentals** - CV model, views, admin interface, comprehensive tests
2. **PDF Generation** - Professional PDF generation with ReportLab
3. **REST API** - Full CRUD operations with DRF, validation, error handling
4. **Middleware & Logging** - Custom request logging middleware
5. **Context Processors** - Dynamic template context injection
6. **Docker Basics** - Containerized development with PostgreSQL
7. **Celery Basics** - Background task processing with Redis
8. **OpenAI Integration** - AI-powered translation service (27 languages)
9. **Deployment** - Production deployment on Railway

## 🔧 **Quick Start**

### **Local Development**
```bash
# Clone repository
git clone <repository-url>
cd DTEAM-django-practical-test

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Load sample data
python manage.py loaddata main/fixtures/sample_cv.json

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### **Docker Development**
```bash
# Build and start services
docker-compose up --build

# Access application
# http://localhost:8000
```

## 📊 **Test Coverage**

- **46+ Tests** covering all major functionality
- Model tests, view tests, API tests
- Middleware tests, context processor tests
- PDF generation tests, error handling tests

Run tests: `python manage.py test main`

## 🚀 **Production Deployment**

The application is deployed on Railway with:
- PostgreSQL database
- Redis for background tasks
- Static file serving via WhiteNoise
- Automatic deployment from Git
- Environment variable management

## 📁 **Project Structure**

```
DTEAM-django-practical-test/
├── CVProject/                 # Django project settings
├── main/                      # Main application
│   ├── models.py             # CV and RequestLog models
│   ├── views.py              # List and detail views
│   ├── api_views.py          # REST API views
│   ├── admin.py              # Admin interface
│   ├── middleware.py         # Request logging middleware
│   ├── context_processors.py # Settings context processor
│   ├── tasks.py              # Celery background tasks
│   ├── translation_service.py # OpenAI translation service
│   ├── tests.py              # Comprehensive test suite
│   └── templates/main/        # HTML templates
├── docker-compose.yml        # Docker development setup
├── docker-compose.prod.yml   # Production Docker setup
├── Dockerfile               # Application container
├── requirements.txt         # Python dependencies
├── railway_startup.py       # Railway deployment script
└── README.md               # This file
```

## 🎨 **Key Features**

### **CV Management**
- Professional CV model with comprehensive fields
- Beautiful list and detail views with pagination
- Admin interface with search and filtering
- Print-friendly templates

### **PDF Generation**
- Professional PDF generation using ReportLab
- Custom styling and formatting
- Automatic filename generation
- Download functionality

### **REST API**
- Complete CRUD operations
- Field validation and error handling
- JSON serialization
- Proper HTTP status codes

### **Background Tasks**
- Celery integration with Redis
- Email notification system
- PDF generation in background
- Task monitoring interface

### **AI Translation**
- OpenAI integration
- Support for 27 languages
- Translation caching
- Real-time translation interface

### **Request Logging**
- Comprehensive request tracking
- Performance monitoring
- User authentication tracking
- Admin interface for logs

## 🔒 **Security Features**

- CSRF protection
- XSS protection headers
- Secure cookie settings
- Input validation
- SQL injection prevention

## 📈 **Performance & Scalability**

- Database query optimization
- Static file compression
- Background task processing
- Translation caching
- Request logging for monitoring

## 🎯 **Demonstrated Skills**

- **Django Development**: Models, views, templates, admin
- **API Development**: RESTful APIs with DRF
- **Background Processing**: Celery task queues
- **AI Integration**: OpenAI API integration
- **DevOps**: Docker, cloud deployment
- **Testing**: Comprehensive test suite
- **Security**: Production-ready security measures

## 📞 **Contact**

**Repository**: [GitHub URL]  
**Live Demo**: https://dteam-django-practical-test-production.up.railway.app

*Ready for technical review and interview discussion.*
