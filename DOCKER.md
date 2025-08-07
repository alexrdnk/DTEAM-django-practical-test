# Docker Setup for CV Project

This document explains how to run the CV Project using Docker and Docker Compose.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DTEAM-django-practical-test
   ```

2. **Environment Files**
   - `.env` - For local development (uses SQLite)
   - `.env.docker` - For Docker environment (uses PostgreSQL)

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Web application: http://localhost:8000
   - Admin interface: http://localhost:8000/admin
   - API endpoints: http://localhost:8000/api/cvs/
   - Settings page: http://localhost:8000/settings/
   - Request logs: http://localhost:8000/logs/

## Default Credentials

- **Admin username**: `admin`
- **Admin password**: `adminpass123`

## Services

### Web Application (Django)
- **Port**: 8000
- **Image**: Built from local Dockerfile
- **Database**: PostgreSQL (in Docker)
- **Features**: 
  - CV management
  - PDF generation
  - REST API
  - Request logging
  - Settings display

### Database (PostgreSQL)
- **Port**: 5432
- **Image**: postgres:15
- **Database**: cvproject_db
- **User**: cvproject_user
- **Password**: cvproject_password

## Environment Configuration

### Local Development (.env)
```bash
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key-here-change-in-production
DB_NAME=cvproject_db
DB_USER=cvproject_user
DB_PASSWORD=cvproject_password
DB_HOST=localhost
DB_PORT=5432
USE_SQLITE=True  # Uses SQLite for local development
```

### Docker Environment (.env.docker)
```bash
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key-here-change-in-production
DB_NAME=cvproject_db
DB_USER=cvproject_user
DB_PASSWORD=cvproject_password
DB_HOST=db
DB_PORT=5432
USE_SQLITE=False  # Uses PostgreSQL in Docker
```

## Docker Commands

### Start services
```bash
docker-compose up
```

### Start services in background
```bash
docker-compose up -d
```

### Stop services
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs
```

### View logs for specific service
```bash
docker-compose logs web
docker-compose logs db
```

### Rebuild and start
```bash
docker-compose up --build
```

### Access Django shell
```bash
docker-compose exec web python manage.py shell
```

### Run Django management commands
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
docker-compose exec web python manage.py createsuperuser
```

### Access PostgreSQL
```bash
docker-compose exec db psql -U cvproject_user -d cvproject_db
```

## Development

### Local Development with SQLite
If you want to run the project locally without Docker:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. The `.env` file is already configured for SQLite:
   ```bash
   USE_SQLITE=True
   ```

3. Run migrations and start server:
   ```bash
   python manage.py migrate
   python manage.py loaddata main/fixtures/sample_cv.json
   python manage.py runserver
   ```

### Docker Development with PostgreSQL
For Docker development with PostgreSQL:

1. Use the `.env.docker` file (already configured)
2. Run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

## Database Configuration

### Local Development
- **Database**: SQLite (`db.sqlite3`)
- **Configuration**: Uses `.env` file with `USE_SQLITE=True`
- **Purpose**: Quick local development and testing

### Docker Environment
- **Database**: PostgreSQL 15
- **Configuration**: Uses `.env.docker` file with `USE_SQLITE=False`
- **Purpose**: Production-like environment with PostgreSQL

## Production Considerations

1. **Security**:
   - Change the SECRET_KEY in production
   - Set DEBUG=False
   - Use strong database passwords
   - Configure ALLOWED_HOSTS properly

2. **Database**:
   - Use external PostgreSQL service
   - Set up proper backups
   - Configure connection pooling

3. **Static Files**:
   - Use a reverse proxy (nginx)
   - Configure static file serving
   - Set up CDN for production

4. **Environment Variables**:
   - Use proper environment variable management
   - Never commit sensitive data
   - Use secrets management in production

## Troubleshooting

### Database Connection Issues
If the web service can't connect to the database:
1. Check if PostgreSQL container is running: `docker-compose ps`
2. Check database logs: `docker-compose logs db`
3. Ensure environment variables are set correctly

### Port Conflicts
If port 8000 or 5432 is already in use:
1. Stop conflicting services
2. Or modify ports in docker-compose.yml

### Permission Issues
If you encounter permission issues:
1. Ensure Docker has proper permissions
2. Check file ownership in the project directory

### Build Issues
If the Docker build fails:
1. Check Dockerfile syntax
2. Ensure all required files are present
3. Check internet connection for downloading images

### Local Development Issues
If you can't run the server locally:
1. Ensure `USE_SQLITE=True` in `.env`
2. Check that all dependencies are installed
3. Run `python manage.py migrate` to create SQLite database 