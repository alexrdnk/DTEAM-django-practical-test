web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn CVProject.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
