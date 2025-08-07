# DTEAM - Django Developer Practical Test

Welcome! This test will help us see how you structure a Django project, work with various tools, and handle common tasks in web development. Follow the instructions step by step. Good luck!

## Project Setup Instructions

### Prerequisites
- Python 3.11+ (managed with pyenv)
- Poetry for dependency management

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DTEAM-django-practical-test
   ```

2. **Set up Python version with pyenv**
   ```bash
   pyenv install 3.11.7
   pyenv local 3.11.7
   ```

3. **Install dependencies with Poetry**
   ```bash
   poetry install
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Load sample data**
   ```bash
   python manage.py loaddata main/fixtures/sample_cv.json
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

### Running the Application

1. **Start the development server**
   ```bash
   python manage.py runserver
   ```

2. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

### Running Tests

```bash
python manage.py test main
```

### Project Structure

```
DTEAM-django-practical-test/
├── CVProject/                 # Django project settings
├── main/                      # Main application
│   ├── models.py             # CV model definition
│   ├── views.py              # List and detail views
│   ├── admin.py              # Admin interface configuration
│   ├── tests.py              # Test cases
│   ├── urls.py               # URL routing
│   ├── templates/main/        # HTML templates
│   ├── fixtures/             # Sample data
│   └── templatetags/         # Custom template filters
├── manage.py                  # Django management script
├── pyproject.toml            # Poetry dependencies
└── .python-version           # Python version specification
```

## Requirements

Follow PEP 8 and other style guidelines, use clear and concise commit messages and docstrings where needed, structure your project for readability and maintainability, optimize database access using Django's built-in methods, and provide enough details in your README.

## Version Control System

1. Create a **public GitHub repository** for this practical test, for example: `DTEAM-django-practical-test`.

2. Put the text of this test (all instructions) into `README.md`.

3. For each task, create a **separate branch** (for example, `tasks/task-1`, `tasks/task-2`, etc.).

4. When you finish each task, **merge** that branch back into `main` but **do not delete the original task branch**.

## Python Virtual Environment

1. Use **pyenv** to manage the Python version. Create a file named `.python-version` in your repository to store the exact Python version.

2. Use **Poetry** to manage and store project dependencies. This will create a `pyproject.toml` file.

3. Update your `README.md` with clear instructions on how to set up and use pyenv and Poetry for this project.

## Tasks

### Task 1: Django Fundamentals ✅ COMPLETED

**Status**: ✅ Completed

**What was implemented**:
1. ✅ **Django Project**: Created `CVProject` using Django 5.2.5
2. ✅ **CV Model**: Created comprehensive CV model with fields: `firstname`, `lastname`, `skills`, `projects`, `bio`, `contacts`, `created_at`, `updated_at`
3. ✅ **Admin Interface**: Configured Django admin with organized fieldsets and search functionality
4. ✅ **Fixtures**: Created sample data with 2 realistic CV entries
5. ✅ **List View**: Implemented efficient list view with pagination and modern UI using Bootstrap
6. ✅ **Detail View**: Created detailed CV view with print functionality
7. ✅ **Templates**: Built responsive templates with modern design using Bootstrap 5 and Font Awesome
8. ✅ **Tests**: Comprehensive test suite covering models, views, and admin functionality (13 tests passing)
9. ✅ **URL Routing**: Proper URL patterns for list and detail views
10. ✅ **Custom Template Filters**: Created custom filters for better template functionality

**Features**:
- Modern, responsive UI with Bootstrap 5
- Efficient database queries with proper ordering
- Pagination for large datasets
- Print-friendly CV detail pages
- Comprehensive admin interface
- Custom template filters for enhanced display
- Full test coverage

**URLs**:
- `/` - CV list page
- `/cv/<id>/` - CV detail page
- `/admin/` - Admin interface

1. **Create a New Django Project**
   - Name it something like `CVProject`.
   - Use the Python version set up in Task 2 and the latest stable Django release.
   - Use **SQLite** as your database for now.

2. **Create an App and Model**
   - Create a Django app (for example, `main`).
   - Define a CV model with fields like `firstname`, `lastname`, `skills`, `projects`, `bio`, and `contacts`.
   - Organize the data in a way that feels efficient and logical.

3. **Load Initial Data with Fixtures**
   - Create a fixture that contains at least one sample CV instance.
   - Include instructions in `README.md` on how to load the fixture.

4. **List Page View and Template**
   - Implement a view for the main page (e.g., `/`) to display a list of CV entries.
   - Use any CSS library to style them nicely.
   - Ensure the data is retrieved from the database efficiently.

5. **Detail Page View**
   - Implement a detail view (e.g., `/cv/<id>/`) to show all data for a single CV.
   - Style it nicely and ensure efficient data retrieval.

6. **Tests**
   - Add basic tests for the list and detail views.
   - Update `README.md` with instructions on how to run these tests.

### Task 2: PDF Generation Basics ✅ COMPLETED

**Status**: ✅ Completed

**What was implemented**:
1. ✅ **PDF Library**: Installed and configured ReportLab for PDF generation
2. ✅ **PDF Generation**: Created comprehensive PDF generation functionality using ReportLab
3. ✅ **Download Button**: Added "Download PDF" button on CV detail page
4. ✅ **PDF Template**: Created PDF-optimized template with professional styling
5. ✅ **URL Routing**: Added PDF download URL pattern (`/cv/<id>/pdf/`)
6. ✅ **Tests**: Added comprehensive tests for PDF functionality (4 new tests, 17 total)

**Features**:
- Professional PDF generation with ReportLab
- Clean, formatted PDF layout with proper styling
- Automatic filename generation based on CV name
- Proper content type and headers for download
- Error handling for non-existent CVs
- Comprehensive test coverage

**Technical Details**:
- Uses ReportLab for reliable PDF generation
- Custom styling with professional fonts and colors
- Proper page layout and spacing
- Includes metadata and generation timestamp
- Windows-compatible (no external dependencies)

**URLs**:
- `/cv/<id>/pdf/` - PDF download endpoint

### Task 3: REST API Fundamentals ✅ COMPLETED

**Status**: ✅ Completed

**What was implemented**:
1. ✅ **Django REST Framework**: Installed and configured DRF for API development
2. ✅ **API Serializers**: Created comprehensive serializers with validation
3. ✅ **CRUD Endpoints**: Implemented full CRUD operations (Create, Read, Update, Delete)
4. ✅ **API Views**: Created both class-based and function-based API views
5. ✅ **URL Routing**: Added API URL patterns for all CRUD operations
6. ✅ **Validation**: Implemented field validation for bio and contacts
7. ✅ **Tests**: Added comprehensive API tests (11 new tests, 24 total)

**Features**:
- Full CRUD API operations for CV model
- Comprehensive field validation
- Both class-based and function-based views
- Proper HTTP status codes and responses
- API serialization with nested data
- Error handling for invalid data
- 404 handling for non-existent resources

**Technical Details**:
- Uses Django REST Framework 3.16.1
- Class-based views: `ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`
- Function-based views with `@api_view` decorator
- Custom serializers with validation methods
- Proper HTTP status codes (200, 201, 204, 400, 404)
- JSON response format

**API Endpoints**:
- `GET /api/cvs/` - List all CVs
- `POST /api/cvs/` - Create new CV
- `GET /api/cvs/<id>/` - Get specific CV
- `PUT /api/cvs/<id>/` - Update specific CV
- `DELETE /api/cvs/<id>/` - Delete specific CV

**Alternative Endpoints**:
- `GET /api/v1/cvs/` - Function-based list API
- `POST /api/v1/cvs/` - Function-based create API
- `GET /api/v1/cvs/<id>/` - Function-based detail API
- `PUT /api/v1/cvs/<id>/` - Function-based update API
- `DELETE /api/v1/cvs/<id>/` - Function-based delete API

**Validation Rules**:
- Bio must be at least 10 characters long
- Contacts cannot be empty
- All required fields must be provided

**Test Coverage**:
- API GET requests (list and detail)
- API POST requests (create)
- API PUT requests (update)
- API DELETE requests (delete)
- Field validation testing
- 404 error handling
- Response format validation

### Task 4: Middleware & Request Logging ✅ COMPLETED

**Status**: ✅ Completed

**What was implemented**:
1. ✅ **RequestLog Model**: Created comprehensive model to track HTTP requests
2. ✅ **Logging Middleware**: Implemented custom middleware to intercept and log requests
3. ✅ **Recent Requests Page**: Created view and template to display logged requests
4. ✅ **Admin Interface**: Added RequestLog to admin with proper configuration
5. ✅ **Database Migration**: Created and applied migration for RequestLog model
6. ✅ **Tests**: Added comprehensive tests for logging functionality (13 new tests, 37 total)

**Features**:
- Automatic logging of all HTTP requests
- Detailed request information (method, path, status, response time)
- User authentication tracking
- IP address and user agent logging
- Performance monitoring with response time tracking
- Admin interface for viewing logs
- Recent requests page with statistics

**Technical Details**:
- Uses Django middleware for request interception
- Efficient database logging with proper indexing
- Response time calculation in milliseconds/seconds
- User authentication status tracking
- Query string and user agent capture
- Error handling to prevent logging failures

**Model Fields**:
- `timestamp`: Request timestamp
- `method`: HTTP method (GET, POST, etc.)
- `path`: Request path
- `query_string`: URL query parameters
- `remote_ip`: Client IP address
- `user_agent`: Browser/client information
- `response_status`: HTTP status code
- `response_time`: Response time in seconds
- `user`: Associated user (if authenticated)
- `is_authenticated`: Authentication status

**URLs**:
- `/logs/` - Recent request logs page
- `/admin/main/requestlog/` - Admin interface for logs

**Admin Features**:
- Read-only log entries (no manual creation/editing)
- Filtering by method, status, authentication
- Search by path, IP, user agent
- Proper ordering by timestamp

**Test Coverage**:
- RequestLog model creation and methods
- Middleware request logging
- Authenticated vs anonymous requests
- API request logging
- Error response logging
- View template and context testing
- Admin interface accessibility

### Task 5: Template Context Processors ✅ COMPLETED

**Status**: ✅ Completed

**What was implemented**:
1. ✅ **Settings Context Processor**: Created `settings_context` to inject Django settings into all templates
2. ✅ **Settings Page**: Created comprehensive settings display page with organized sections
3. ✅ **Context Processor Registration**: Added context processor to Django settings
4. ✅ **Settings View**: Created view to display settings values
5. ✅ **Settings Template**: Built beautiful template with Bootstrap styling and organized sections
6. ✅ **Tests**: Added comprehensive tests for context processor and settings page (9 new tests, 46 total)

**Features**:
- Automatic injection of Django settings into all templates
- Comprehensive settings display page with organized sections
- Security-conscious SECRET_KEY truncation
- Beautiful Bootstrap-styled settings interface
- Organized display of all major Django settings
- Color-coded status indicators for boolean settings

**Technical Details**:
- Context processor makes settings available in all templates
- Settings page displays DEBUG, SECRET_KEY, INSTALLED_APPS, MIDDLEWARE, etc.
- Proper handling of optional settings (MEDIA_URL)
- SECRET_KEY truncation for security
- Organized display with cards and badges

**Available Settings in Templates**:
- `settings`: Full Django settings object
- `DEBUG`: Debug mode status
- `SECRET_KEY`: Truncated secret key for security
- `INSTALLED_APPS`: List of installed applications
- `MIDDLEWARE`: List of middleware classes
- `ROOT_URLCONF`: URL configuration module
- `TEMPLATES`: Template configuration
- `WSGI_APPLICATION`: WSGI application path
- `STATIC_URL`: Static files URL
- `MEDIA_URL`: Media files URL (if set)
- `LANGUAGE_CODE`: Language code
- `TIME_ZONE`: Time zone setting
- `USE_I18N`: Internationalization status
- `USE_TZ`: Time zone support status
- `DEFAULT_AUTO_FIELD`: Default auto field setting

**URLs**:
- `/settings/` - Django settings display page

**Template Features**:
- Color-coded status badges for boolean settings
- Organized sections for different setting categories
- Responsive design with Bootstrap
- Code formatting for technical values
- Security-conscious display of sensitive information

**Test Coverage**:
- Context processor functionality testing
- Settings availability in templates
- SECRET_KEY truncation testing
- Settings page view testing
- Template context validation
- Settings data type validation

### Task 6: Docker Basics ✅ COMPLETED

**Status**: ✅ Completed

**What was implemented**:
1. ✅ **Docker Compose Setup**: Created comprehensive Docker Compose configuration
2. ✅ **PostgreSQL Database**: Switched from SQLite to PostgreSQL in Docker
3. ✅ **Environment Variables**: Implemented .env file for configuration
4. ✅ **Dockerfile**: Created optimized Dockerfile for Django application
5. ✅ **Docker Documentation**: Created comprehensive DOCKER.md with instructions
6. ✅ **Management Command**: Created setup_docker command for automated setup
7. ✅ **Tests**: Added Docker setup tests (51 total tests)

**Features**:
- Complete Docker containerization with PostgreSQL
- Environment variable management with python-decouple
- Automated database setup and migrations
- Health checks for database service
- Non-root user for security
- Comprehensive documentation

**Technical Details**:
- **Dockerfile**: Python 3.11-slim base, PostgreSQL client, non-root user
- **Docker Compose**: Web service + PostgreSQL database with health checks
- **Environment Variables**: DEBUG, SECRET_KEY, DB_* variables
- **Database**: PostgreSQL 15 with persistent volume
- **Setup Command**: Automated migrations, data loading, superuser creation

**Docker Services**:
- **Web Application**: Django app on port 8000
- **Database**: PostgreSQL 15 on port 5432
- **Volumes**: Persistent PostgreSQL data

**Environment Variables**:
- `DEBUG`: Django debug mode
- `SECRET_KEY`: Django secret key
- `DB_NAME`: PostgreSQL database name
- `DB_USER`: PostgreSQL username
- `DB_PASSWORD`: PostgreSQL password
- `DB_HOST`: Database host (default: db)
- `DB_PORT`: Database port (default: 5432)
- `USE_SQLITE`: Fallback to SQLite (for local development)

**Docker Commands**:
```bash
# Build and start services
docker-compose up --build

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs

# Access Django shell
docker-compose exec web python manage.py shell

# Run migrations
docker-compose exec web python manage.py migrate
```

**Local Development**:
- Set `USE_SQLITE=True` to use SQLite instead of PostgreSQL
- Install dependencies: `pip install -r requirements.txt`
- Run with SQLite: `python manage.py runserver`

**Test Coverage**:
- Docker setup and environment variable handling
- Database configuration testing
- Environment variable loading
- Settings configuration validation

### Task 7: Celery Basics ✅ COMPLETED

**Status**: ✅ Completed

**What was implemented**:
1. ✅ **Celery Installation**: Installed Celery and Redis for background task processing
2. ✅ **Celery Configuration**: Created comprehensive Celery setup with Redis broker
3. ✅ **Docker Integration**: Added Redis and Celery services to docker-compose.yml
4. ✅ **CV Detail Page Enhancement**: Added email input field and 'Send PDF to Email' button
5. ✅ **Background Task**: Implemented Celery task to send CV PDF via email

**Features**:
- Complete Celery setup with Redis message broker
- Docker Compose configuration with Redis and Celery workers
- Email input field on CV detail page
- 'Send PDF to Email' button that triggers background task
- Real-time feedback with loading states and success/error messages

**Technical Details**:
- **Celery Configuration**: Redis broker, JSON serialization, UTC timezone
- **Docker Services**: Redis 7, Celery worker, Celery Beat scheduler
- **Background Task**: `send_cv_notification_task` for emailing CV PDFs
- **Frontend**: AJAX form submission with CSRF protection
- **Error Handling**: Graceful failure handling for all scenarios

**Background Tasks Implemented**:
- `send_cv_notification_task`: Send CV PDF via email (Task 7 requirement)
- `send_email_task`: General email sending functionality
- `generate_cv_pdf_task`: Generate PDFs in background
- `cleanup_old_logs_task`: Clean up old request logs
- `send_daily_report_task`: Send daily system reports
- `test_task`: Simple test task for debugging
- `long_running_task`: Simulate long-running processes

**Docker Services**:
- **Redis**: Message broker on port 6379
- **Celery Worker**: Processes background tasks
- **Celery Beat**: Scheduler for periodic tasks
- **Web**: Django application with enhanced CV detail page

**Task 7 Implementation**:
- **Email Input Field**: Added to CV detail page with validation
- **Send PDF Button**: Triggers Celery task to email CV PDF
- **Real-time Feedback**: Shows loading state and success/error messages
- **Background Processing**: PDF generation and email sending happen asynchronously

**URLs**:
- `/cv/<id>/` - CV detail page with email functionality
- `/api/send-pdf-email/` - API endpoint for sending PDF to email

**Test Coverage**:
- Celery task functionality testing
- Email form submission testing
- Task error handling testing
- Docker service integration testing

### Task 8: OpenAI Basics

1. On the CV detail page, add a 'Translate' button and a language selector.

2. Include these languages: Cornish, Manx, Breton, Inuktitut, Kalaallisut, Romani, Occitan, Ladino, Northern Sami, Upper Sorbian, Kashubian, Zazaki, Chuvash, Livonian, Tsakonian, Saramaccan, Bislama.

3. Hook this up to an OpenAI translation API or any other translation mechanism you prefer. The idea is to translate the CV content into the selected language.

### Task 9: Deployment

Deploy this project to DigitalOcean or any other VPS. (If you do not have a DigitalOcean account, you can use this referral link to create account with $200 on balance: https://m.do.co/c/967939ea1e74)

## That's it!

Complete each task thoroughly, commit your work following the branch-and-merge structure, and make sure your `README.md` clearly explains how to install, run, and test everything. We look forward to reviewing your submission!

Thank you!
