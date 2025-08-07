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

### Task 3: REST API Fundamentals

1. Install **Django REST Framework** (DRF).

2. Create CRUD endpoints for the CV model (create, retrieve, update, delete).

3. Add tests to verify that each CRUD action works correctly.

### Task 4: Middleware & Request Logging

1. **Create a RequestLog Model**
   - You can put this in the existing app or a new app (e.g., `audit`).
   - Include fields such as `timestamp`, `HTTP method`, `path`, and optionally other details like query string, remote IP, or logged-in user.

2. **Implement Logging Middleware**
   - Write a custom Django middleware class that intercepts each incoming request.
   - Create a RequestLog record in the database with the relevant request data.
   - Keep it efficient.

3. **Recent Requests Page**
   - Create a view (e.g., `/logs/`) showing the 10 most recent logged requests, sorted by timestamp descending.
   - Include a template that loops through these entries and displays their timestamp, method, and path.

4. **Test Logging**
   - Ensure your tests verify the logging functionality.

### Task 5: Template Context Processors

1. **Create settings_context**
   - Create a context processor that injects your entire Django settings into all templates.

2. **Settings Page**
   - Create a view (e.g., `/settings/`) that displays `DEBUG` and other settings values made available by the context processor.

### Task 6: Docker Basics

1. Use Docker Compose to containerize your project.

2. Switch the database from SQLite to PostgreSQL in Docker Compose.

3. Store all necessary environment variables (database credentials, etc.) in a `.env` file.

### Task 7: Celery Basics

1. Install and configure **Celery**, using Redis or RabbitMQ as the broker.

2. Add a Celery worker to your Docker Compose configuration.

3. On the CV detail page, add an email input field and a 'Send PDF to Email' button to trigger a Celery task that emails the PDF.

### Task 8: OpenAI Basics

1. On the CV detail page, add a 'Translate' button and a language selector.

2. Include these languages: Cornish, Manx, Breton, Inuktitut, Kalaallisut, Romani, Occitan, Ladino, Northern Sami, Upper Sorbian, Kashubian, Zazaki, Chuvash, Livonian, Tsakonian, Saramaccan, Bislama.

3. Hook this up to an OpenAI translation API or any other translation mechanism you prefer. The idea is to translate the CV content into the selected language.

### Task 9: Deployment

Deploy this project to DigitalOcean or any other VPS. (If you do not have a DigitalOcean account, you can use this referral link to create account with $200 on balance: https://m.do.co/c/967939ea1e74)

## That's it!

Complete each task thoroughly, commit your work following the branch-and-merge structure, and make sure your `README.md` clearly explains how to install, run, and test everything. We look forward to reviewing your submission!

Thank you!
