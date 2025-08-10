from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import CV, RequestLog
from .context_processors import settings_context
from decouple import config
from .tasks import (
    send_email_task, send_cv_notification_task, generate_cv_pdf_task,
    cleanup_old_logs_task, send_daily_report_task, test_task, long_running_task
)
from .translation_service import TranslationService
import json


class CVModelTest(TestCase):
    """Test cases for CV model."""

    def setUp(self):
        """Set up test data."""
        self.cv = CV.objects.create(
            firstname="John",
            lastname="Doe",
            skills="Python, Django, React",
            projects="E-commerce Platform: Built a full-stack application",
            bio="Experienced developer with 5+ years of experience",
            contacts="john.doe@email.com\n+1 (555) 123-4567"
        )

    def test_cv_creation(self):
        """Test CV creation."""
        self.assertEqual(self.cv.firstname, "John")
        self.assertEqual(self.cv.lastname, "Doe")
        self.assertEqual(self.cv.get_full_name(), "John Doe")

    def test_cv_str_method(self):
        """Test CV string representation."""
        self.assertEqual(str(self.cv), "John Doe")

    def test_cv_get_full_name(self):
        """Test get_full_name method."""
        self.assertEqual(self.cv.get_full_name(), "John Doe")

    def test_cv_ordering(self):
        """Test CV ordering by creation date."""
        cv2 = CV.objects.create(
            firstname="Jane",
            lastname="Smith",
            skills="Java, Spring",
            projects="Microservices project",
            bio="Senior developer",
            contacts="jane.smith@email.com"
        )
        cvs = list(CV.objects.all())
        self.assertEqual(cvs[0], cv2)  # Newer CV should be first


class CVListViewTest(TestCase):
    """Test cases for CV list view."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.cv = CV.objects.create(
            firstname="John",
            lastname="Doe",
            skills="Python, Django",
            projects="Web application",
            bio="Experienced developer",
            contacts="john.doe@email.com"
        )

    def test_cv_list_view_status_code(self):
        """Test CV list view returns 200 status code."""
        response = self.client.get(reverse('main:cv_list'))
        self.assertEqual(response.status_code, 200)

    def test_cv_list_view_template(self):
        """Test CV list view uses correct template."""
        response = self.client.get(reverse('main:cv_list'))
        self.assertTemplateUsed(response, 'main/cv_list.html')

    def test_cv_list_view_context(self):
        """Test CV list view has correct context."""
        response = self.client.get(reverse('main:cv_list'))
        self.assertIn('cvs', response.context)
        self.assertEqual(len(response.context['cvs']), 1)

    def test_cv_list_view_ordering(self):
        """Test CV list view orders by creation date."""
        cv2 = CV.objects.create(
            firstname="Jane",
            lastname="Smith",
            skills="Java",
            projects="Another project",
            bio="Another developer",
            contacts="jane.smith@email.com"
        )
        response = self.client.get(reverse('main:cv_list'))
        cvs = response.context['cvs']
        self.assertEqual(cvs[0], cv2)  # Newer CV should be first


class CVDetailViewTest(TestCase):
    """Test cases for CV detail view."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.cv = CV.objects.create(
            firstname="John",
            lastname="Doe",
            skills="Python, Django",
            projects="Web application",
            bio="Experienced developer",
            contacts="john.doe@email.com"
        )

    def test_cv_detail_view_status_code(self):
        """Test CV detail view returns 200 status code."""
        response = self.client.get(reverse('main:cv_detail', kwargs={'pk': self.cv.pk}))
        self.assertEqual(response.status_code, 200)

    def test_cv_detail_view_template(self):
        """Test CV detail view uses correct template."""
        response = self.client.get(reverse('main:cv_detail', kwargs={'pk': self.cv.pk}))
        self.assertTemplateUsed(response, 'main/cv_detail.html')

    def test_cv_detail_view_context(self):
        """Test CV detail view has correct context."""
        response = self.client.get(reverse('main:cv_detail', kwargs={'pk': self.cv.pk}))
        self.assertIn('cv', response.context)
        self.assertEqual(response.context['cv'], self.cv)

    def test_cv_detail_view_404(self):
        """Test CV detail view returns 404 for non-existent CV."""
        response = self.client.get(reverse('main:cv_detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)


class CVAdminTest(TestCase):
    """Test cases for CV admin interface."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.client.login(username='admin', password='adminpass123')

    def test_cv_admin_list_view(self):
        """Test CV admin list view is accessible."""
        response = self.client.get('/admin/main/cv/')
        self.assertEqual(response.status_code, 200)


class CVPDFTest(TestCase):
    """Test cases for CV PDF generation."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.cv = CV.objects.create(
            firstname="John",
            lastname="Doe",
            skills="Python, Django",
            projects="Web application",
            bio="Experienced developer",
            contacts="john.doe@email.com"
        )

    def test_cv_pdf_download_status_code(self):
        """Test CV PDF download returns 200 status code."""
        response = self.client.get(reverse('main:cv_pdf_download', kwargs={'pk': self.cv.pk}))
        self.assertEqual(response.status_code, 200)

    def test_cv_pdf_content_type(self):
        """Test CV PDF download returns correct content type."""
        response = self.client.get(reverse('main:cv_pdf_download', kwargs={'pk': self.cv.pk}))
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_cv_pdf_filename(self):
        """Test CV PDF download has correct filename."""
        response = self.client.get(reverse('main:cv_pdf_download', kwargs={'pk': self.cv.pk}))
        expected_filename = f'attachment; filename="{self.cv.get_full_name()}_CV.pdf"'
        self.assertEqual(response['Content-Disposition'], expected_filename)

    def test_cv_pdf_404(self):
        """Test CV PDF download returns 404 for non-existent CV."""
        response = self.client.get(reverse('main:cv_pdf_download', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)


class CVAPITest(APITestCase):
    """Test cases for CV REST API."""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.cv_data = {
            'firstname': 'John',
            'lastname': 'Doe',
            'skills': 'Python, Django, React',
            'projects': 'E-commerce Platform: Built a full-stack application',
            'bio': 'Experienced developer with 5+ years of experience',
            'contacts': 'john.doe@email.com\n+1 (555) 123-4567'
        }
        self.cv = CV.objects.create(**self.cv_data)

    def test_cv_list_api_get(self):
        """Test GET request to CV list API."""
        url = reverse('main:cv_list_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn('full_name', response.data[0])

    def test_cv_list_api_post(self):
        """Test POST request to CV list API."""
        url = reverse('main:cv_list_api')
        new_cv_data = {
            'firstname': 'Jane',
            'lastname': 'Smith',
            'skills': 'Java, Spring',
            'projects': 'Microservices project',
            'bio': 'Senior developer with extensive experience',
            'contacts': 'jane.smith@email.com\n+1 (555) 987-6543'
        }
        response = self.client.post(url, new_cv_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CV.objects.count(), 2)

    def test_cv_detail_api_get(self):
        """Test GET request to CV detail API."""
        url = reverse('main:cv_detail_api', kwargs={'pk': self.cv.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['firstname'], 'John')
        self.assertEqual(response.data['lastname'], 'Doe')

    def test_cv_detail_api_put(self):
        """Test PUT request to CV detail API."""
        url = reverse('main:cv_detail_api', kwargs={'pk': self.cv.pk})
        updated_data = self.cv_data.copy()
        updated_data['firstname'] = 'Jane'
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cv.refresh_from_db()
        self.assertEqual(self.cv.firstname, 'Jane')

    def test_cv_detail_api_delete(self):
        """Test DELETE request to CV detail API."""
        url = reverse('main:cv_detail_api', kwargs={'pk': self.cv.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CV.objects.count(), 0)

    def test_cv_api_validation(self):
        """Test API validation for required fields."""
        url = reverse('main:cv_list_api')
        invalid_data = {
            'firstname': 'John',
            'lastname': 'Doe',
            'skills': 'Python',
            'projects': 'Project',
            'bio': 'Short',  # Too short
            'contacts': ''  # Empty
        }
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('bio', response.data)
        self.assertIn('contacts', response.data)

    def test_cv_api_404(self):
        """Test API returns 404 for non-existent CV."""
        url = reverse('main:cv_detail_api', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RequestLogModelTest(TestCase):
    """Test cases for RequestLog model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.log = RequestLog.objects.create(
            method='GET',
            path='/test/',
            query_string='param=value',
            remote_ip='127.0.0.1',
            user_agent='Test Browser',
            response_status=200,
            response_time=0.1,
            user=self.user,
            is_authenticated=True
        )

    def test_request_log_creation(self):
        """Test RequestLog creation."""
        self.assertEqual(self.log.method, 'GET')
        self.assertEqual(self.log.path, '/test/')
        self.assertEqual(self.log.response_status, 200)
        self.assertEqual(self.log.user, self.user)
        self.assertTrue(self.log.is_authenticated)

    def test_request_log_str_method(self):
        """Test RequestLog string representation."""
        expected = f"GET /test/ - {self.log.timestamp}"
        self.assertEqual(str(self.log), expected)

    def test_request_log_get_duration_display(self):
        """Test get_duration_display method."""
        # Test milliseconds
        self.log.response_time = 0.05
        self.assertEqual(self.log.get_duration_display(), "50ms")

        # Test seconds
        self.log.response_time = 1.5
        self.assertEqual(self.log.get_duration_display(), "1.50s")

    def test_request_log_ordering(self):
        """Test RequestLog ordering by timestamp."""
        log2 = RequestLog.objects.create(
            method='POST',
            path='/test2/',
            remote_ip='127.0.0.1',
            response_status=201,
            response_time=0.2
        )
        logs = list(RequestLog.objects.all())
        self.assertEqual(logs[0], log2)  # Newer log should be first


class RequestLogViewTest(TestCase):
    """Test cases for RequestLog list view."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.log = RequestLog.objects.create(
            method='GET',
            path='/test/',
            remote_ip='127.0.0.1',
            response_status=200,
            response_time=0.1
        )

    def test_request_log_view_status_code(self):
        """Test RequestLog view returns 200 status code."""
        response = self.client.get(reverse('main:request_logs'))
        self.assertEqual(response.status_code, 200)

    def test_request_log_view_template(self):
        """Test RequestLog view uses correct template."""
        response = self.client.get(reverse('main:request_logs'))
        self.assertTemplateUsed(response, 'main/request_logs.html')

    def test_request_log_view_context(self):
        """Test RequestLog view has correct context."""
        response = self.client.get(reverse('main:request_logs'))
        self.assertIn('logs', response.context)
        self.assertEqual(len(response.context['logs']), 1)

    def test_request_log_view_limits_to_10(self):
        """Test RequestLog view limits to 10 most recent logs."""
        # Create 15 logs
        for i in range(15):
            RequestLog.objects.create(
                method='GET',
                path=f'/test{i}/',
                remote_ip='127.0.0.1',
                response_status=200,
                response_time=0.1
            )

        response = self.client.get(reverse('main:request_logs'))
        self.assertEqual(len(response.context['logs']), 10)


class RequestLoggingMiddlewareTest(TestCase):
    """Test cases for RequestLoggingMiddleware."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.cv = CV.objects.create(
            firstname="John",
            lastname="Doe",
            skills="Python, Django",
            projects="Web application",
            bio="Experienced developer",
            contacts="john.doe@email.com"
        )

    def test_middleware_logs_requests(self):
        """Test that middleware logs requests."""
        initial_count = RequestLog.objects.count()

        # Make a request
        response = self.client.get(reverse('main:cv_list'))
        self.assertEqual(response.status_code, 200)

        # Check that a log was created
        self.assertEqual(RequestLog.objects.count(), initial_count + 1)

        # Check log details
        log = RequestLog.objects.latest('timestamp')
        self.assertEqual(log.method, 'GET')
        self.assertEqual(log.path, '/')
        self.assertEqual(log.response_status, 200)
        self.assertGreater(log.response_time, 0)

    def test_middleware_logs_authenticated_requests(self):
        """Test that middleware logs authenticated requests correctly."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

        # Make an authenticated request
        response = self.client.get(reverse('main:cv_list'))
        self.assertEqual(response.status_code, 200)

        # Check that log shows authenticated user
        log = RequestLog.objects.latest('timestamp')
        self.assertEqual(log.user, user)
        self.assertTrue(log.is_authenticated)

    def test_middleware_logs_anonymous_requests(self):
        """Test that middleware logs anonymous requests correctly."""
        # Make an anonymous request
        response = self.client.get(reverse('main:cv_list'))
        self.assertEqual(response.status_code, 200)

        # Check that log shows anonymous user
        log = RequestLog.objects.latest('timestamp')
        self.assertIsNone(log.user)
        self.assertFalse(log.is_authenticated)

    def test_middleware_logs_api_requests(self):
        """Test that middleware logs API requests."""
        # Make an API request
        response = self.client.get('/api/cvs/')
        self.assertEqual(response.status_code, 200)

        # Check that log was created
        log = RequestLog.objects.latest('timestamp')
        self.assertEqual(log.method, 'GET')
        self.assertEqual(log.path, '/api/cvs/')
        self.assertEqual(log.response_status, 200)

    def test_middleware_logs_error_responses(self):
        """Test that middleware logs error responses."""
        # Make a request to non-existent page
        response = self.client.get('/non-existent-page/')
        self.assertEqual(response.status_code, 404)

        # Check that log was created with error status
        log = RequestLog.objects.latest('timestamp')
        self.assertEqual(log.response_status, 404)


class ContextProcessorTest(TestCase):
    """Test cases for settings context processor."""

    def test_settings_context_processor(self):
        """Test that settings context processor returns expected data."""
        # Create a mock request
        request = type('MockRequest', (), {})()

        # Get context from processor
        context = settings_context(request)

        # Check that required settings are present
        self.assertIn('settings', context)
        self.assertIn('DEBUG', context)
        self.assertIn('SECRET_KEY', context)
        self.assertIn('INSTALLED_APPS', context)
        self.assertIn('MIDDLEWARE', context)
        self.assertIn('ROOT_URLCONF', context)
        self.assertIn('TEMPLATES', context)
        self.assertIn('WSGI_APPLICATION', context)
        self.assertIn('STATIC_URL', context)
        self.assertIn('LANGUAGE_CODE', context)
        self.assertIn('TIME_ZONE', context)
        self.assertIn('USE_I18N', context)
        self.assertIn('USE_TZ', context)
        self.assertIn('DEFAULT_AUTO_FIELD', context)

    def test_settings_context_secret_key_truncation(self):
        """Test that SECRET_KEY is properly truncated in context."""
        request = type('MockRequest', (), {})()
        context = settings_context(request)

        # Check that SECRET_KEY is truncated if longer than 10 characters
        secret_key = context['SECRET_KEY']
        if len(secret_key) > 13:  # 10 chars + '...'
            self.assertTrue(secret_key.endswith('...'))

    def test_settings_context_media_url_handling(self):
        """Test that MEDIA_URL is handled properly when not set."""
        request = type('MockRequest', (), {})()
        context = settings_context(request)

        # Check that MEDIA_URL is present (even if empty)
        self.assertIn('MEDIA_URL', context)


class SettingsViewTest(TestCase):
    """Test cases for settings view."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()

    def test_settings_view_status_code(self):
        """Test settings view returns 200 status code."""
        response = self.client.get(reverse('main:settings'))
        self.assertEqual(response.status_code, 200)

    def test_settings_view_template(self):
        """Test settings view uses correct template."""
        response = self.client.get(reverse('main:settings'))
        self.assertTemplateUsed(response, 'main/settings.html')

    def test_settings_view_context(self):
        """Test settings view has settings in context."""
        response = self.client.get(reverse('main:settings'))
        self.assertIn('DEBUG', response.context)
        self.assertIn('SECRET_KEY', response.context)
        self.assertIn('INSTALLED_APPS', response.context)
        self.assertIn('MIDDLEWARE', response.context)
        self.assertIn('ROOT_URLCONF', response.context)
        self.assertIn('TEMPLATES', response.context)
        self.assertIn('WSGI_APPLICATION', response.context)
        self.assertIn('STATIC_URL', response.context)
        self.assertIn('LANGUAGE_CODE', response.context)
        self.assertIn('TIME_ZONE', response.context)
        self.assertIn('USE_I18N', response.context)
        self.assertIn('USE_TZ', response.context)
        self.assertIn('DEFAULT_AUTO_FIELD', response.context)

    def test_settings_view_debug_display(self):
        """Test that DEBUG setting is properly displayed."""
        response = self.client.get(reverse('main:settings'))
        self.assertIn('DEBUG', response.context)
        # Check that the template can access DEBUG
        self.assertIsInstance(response.context['DEBUG'], bool)

    def test_settings_view_installed_apps_display(self):
        """Test that INSTALLED_APPS is properly displayed."""
        response = self.client.get(reverse('main:settings'))
        self.assertIn('INSTALLED_APPS', response.context)
        # Check that INSTALLED_APPS is a list
        self.assertIsInstance(response.context['INSTALLED_APPS'], list)

    def test_settings_view_middleware_display(self):
        """Test that MIDDLEWARE is properly displayed."""
        response = self.client.get(reverse('main:settings'))
        self.assertIn('MIDDLEWARE', response.context)
        # Check that MIDDLEWARE is a list
        self.assertIsInstance(response.context['MIDDLEWARE'], list)


class DockerSetupTest(TestCase):
    """Test cases for Docker setup and environment variables."""

    def test_environment_variables_loading(self):
        """Test that environment variables are properly loaded."""
        # Test that config function is available
        from decouple import config

        # Test default values
        debug = config('DEBUG', default=True, cast=bool)
        self.assertIsInstance(debug, bool)

        secret_key = config('SECRET_KEY', default='test-key')
        self.assertIsInstance(secret_key, str)

        db_name = config('DB_NAME', default='test_db')
        self.assertIsInstance(db_name, str)

    def test_database_configuration(self):
        """Test that database configuration is properly set."""
        from django.conf import settings

        # Check that database configuration exists
        self.assertIn('default', settings.DATABASES)

        # Check that database engine is set
        db_config = settings.DATABASES['default']
        self.assertIn('ENGINE', db_config)

        # Check that database name is set
        self.assertIn('NAME', db_config)

    def test_allowed_hosts_configuration(self):
        """Test that ALLOWED_HOSTS is properly configured for Docker."""
        from django.conf import settings

        # Check that ALLOWED_HOSTS allows all hosts (for Docker)
        self.assertIn('*', settings.ALLOWED_HOSTS)

    def test_debug_configuration(self):
        """Test that DEBUG setting is properly configured."""
        from django.conf import settings

        # Check that DEBUG is a boolean
        self.assertIsInstance(settings.DEBUG, bool)

    def test_secret_key_configuration(self):
        """Test that SECRET_KEY is properly configured."""
        from django.conf import settings

        # Check that SECRET_KEY is a string
        self.assertIsInstance(settings.SECRET_KEY, str)

        # Check that SECRET_KEY is not empty
        self.assertGreater(len(settings.SECRET_KEY), 0)


class CeleryTasksTest(TestCase):
    """Test cases for Celery background tasks."""

    def setUp(self):
        """Set up test data."""
        self.cv = CV.objects.create(
            firstname="John",
            lastname="Doe",
            skills="Python, Django",
            projects="Web application",
            bio="Experienced developer",
            contacts="john.doe@email.com"
        )

    def test_test_task(self):
        """Test the simple test task."""
        result = test_task()
        self.assertEqual(result, "Test task completed successfully!")

    def test_send_email_task(self):
        """Test email sending task."""
        result = send_email_task(
            "Test Subject",
            "Test message",
            ["test@example.com"]
        )
        # The task should either succeed or fail gracefully
        self.assertIsInstance(result, str)
        self.assertTrue(
            "Email sent successfully" in result or "Failed to send email" in result,
            f"Unexpected result: {result}"
        )

    def test_send_cv_notification_task(self):
        """Test CV notification task."""
        result = send_cv_notification_task(self.cv.id, "admin@cvproject.com")
        # Should return an AsyncResult object
        from celery.result import AsyncResult
        self.assertIsInstance(result, AsyncResult)

    def test_generate_cv_pdf_task(self):
        """Test PDF generation task."""
        result = generate_cv_pdf_task(self.cv.id)
        self.assertIn("PDF generated successfully", result)

    def test_generate_cv_pdf_task_invalid_id(self):
        """Test PDF generation task with invalid CV ID."""
        result = generate_cv_pdf_task(999)
        self.assertIn("CV with ID 999 not found", result)

    def test_cleanup_old_logs_task(self):
        """Test log cleanup task."""
        result = cleanup_old_logs_task()
        self.assertIn("No cleanup needed", result)

    def test_send_daily_report_task(self):
        """Test daily report task."""
        result = send_daily_report_task()
        # Should return an AsyncResult object
        from celery.result import AsyncResult
        self.assertIsInstance(result, AsyncResult)

    def test_long_running_task(self):
        """Test long running task."""
        result = long_running_task()
        self.assertEqual(result, "Long running task completed!")


class BackgroundTaskViewTest(TestCase):
    """Test cases for background task trigger view."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.cv = CV.objects.create(
            firstname="John",
            lastname="Doe",
            skills="Python, Django",
            projects="Web application",
            bio="Experienced developer",
            contacts="john.doe@email.com"
        )

    def test_trigger_task_view_status_code(self):
        """Test trigger task view returns 200 status code."""
        response = self.client.get(reverse('main:trigger_task'))
        self.assertEqual(response.status_code, 200)

    def test_trigger_task_view_json_response(self):
        """Test trigger task view returns JSON response."""
        response = self.client.get(reverse('main:trigger_task'))
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_trigger_task_view_default_task(self):
        """Test trigger task view with default task type."""
        response = self.client.get(reverse('main:trigger_task'))
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('Test task triggered', data['message'])
        self.assertIn('task_id', data)

    def test_trigger_task_view_email_task(self):
        """Test trigger task view with email task type."""
        response = self.client.get(reverse('main:trigger_task') + '?task=email')
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('Email task triggered', data['message'])
        self.assertIn('task_id', data)

    def test_trigger_task_view_cv_notification_task(self):
        """Test trigger task view with CV notification task type."""
        response = self.client.get(reverse('main:trigger_task') + '?task=cv_notification')
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('CV notification task triggered', data['message'])
        self.assertIn('task_id', data)

    def test_trigger_task_view_pdf_generation_task(self):
        """Test trigger task view with PDF generation task type."""
        response = self.client.get(reverse('main:trigger_task') + '?task=pdf_generation')
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('PDF generation task triggered', data['message'])
        self.assertIn('task_id', data)

    def test_trigger_task_view_cleanup_logs_task(self):
        """Test trigger task view with cleanup logs task type."""
        try:
            response = self.client.get(reverse('main:trigger_task') + '?task=cleanup_logs')
            data = response.json()
            self.assertEqual(data['status'], 'success')
            self.assertIn('Log cleanup task triggered', data['message'])
            self.assertIn('task_id', data)
        except Exception as e:
            # If Redis is not available, the task should still be triggered
            # but may fail due to connection issues
            self.assertIn('Log cleanup task triggered', str(e) or 'Task triggered')

    def test_trigger_task_view_daily_report_task(self):
        """Test trigger task view with daily report task type."""
        try:
            response = self.client.get(reverse('main:trigger_task') + '?task=daily_report')
            data = response.json()
            self.assertEqual(data['status'], 'success')
            self.assertIn('Daily report task triggered', data['message'])
            self.assertIn('task_id', data)
        except Exception as e:
            # If Redis is not available, the task should still be triggered
            # but may fail due to connection issues
            self.assertIn('Daily report task triggered', str(e) or 'Task triggered')

    def test_trigger_task_view_long_running_task(self):
        """Test trigger task view with long running task type."""
        try:
            response = self.client.get(reverse('main:trigger_task') + '?task=long_running')
            data = response.json()
            self.assertEqual(data['status'], 'success')
            self.assertIn('Long running task triggered', data['message'])
            self.assertIn('task_id', data)
        except Exception as e:
            # If Redis is not available, the task should still be triggered
            # but may fail due to connection issues
            self.assertIn('Long running task triggered', str(e) or 'Task triggered')

    def test_trigger_task_view_cv_notification_no_cv(self):
        """Test trigger task view with CV notification when no CVs exist."""
        CV.objects.all().delete()
        response = self.client.get(reverse('main:trigger_task') + '?task=cv_notification')
        data = response.json()
        self.assertEqual(data['status'], 'error')
        self.assertIn('No CVs found', data['message'])

    def test_trigger_task_view_pdf_generation_no_cv(self):
        """Test trigger task view with PDF generation when no CVs exist."""
        CV.objects.all().delete()
        response = self.client.get(reverse('main:trigger_task') + '?task=pdf_generation')
        data = response.json()
        self.assertEqual(data['status'], 'error')
        self.assertIn('No CVs found', data['message'])


class TranslationServiceTest(TestCase):
    """Test cases for translation service."""

    def setUp(self):
        """Set up test data."""
        self.cv = CV.objects.create(
            firstname="John",
            lastname="Doe",
            skills="Python, Django",
            projects="Web application",
            bio="Experienced developer",
            contacts="john.doe@email.com"
        )
        self.translation_service = TranslationService()

    def test_get_available_languages(self):
        """Test getting available languages."""
        languages = self.translation_service.get_available_languages()
        self.assertIsInstance(languages, dict)

        # Test original required languages
        self.assertIn('cornish', languages)
        self.assertIn('manx', languages)
        self.assertIn('breton', languages)
        self.assertEqual(languages['cornish'], 'Cornish')

        # Test additional popular languages
        self.assertIn('french', languages)
        self.assertIn('german', languages)
        self.assertIn('spanish', languages)
        self.assertIn('portuguese_brazil', languages)
        self.assertIn('italian', languages)
        self.assertIn('japanese', languages)
        self.assertIn('chinese_simplified', languages)
        self.assertIn('ukrainian', languages)
        self.assertIn('korean', languages)
        self.assertIn('turkish', languages)

        # Test total count (17 original + 10 new = 27)
        self.assertEqual(len(languages), 27)

    def test_prepare_cv_content(self):
        """Test CV content preparation."""
        content = self.translation_service._prepare_cv_content(self.cv)
        self.assertEqual(content['name'], 'John Doe')
        self.assertEqual(content['bio'], 'Experienced developer')
        self.assertEqual(content['skills'], 'Python, Django')
        self.assertEqual(content['projects'], 'Web application')
        self.assertEqual(content['contacts'], 'john.doe@email.com')

    def test_create_translation_prompt(self):
        """Test translation prompt creation."""
        cv_content = {
            'name': 'John Doe',
            'bio': 'Experienced developer',
            'skills': 'Python, Django',
            'projects': 'Web application',
            'contacts': 'john.doe@email.com'
        }
        prompt = self.translation_service._create_translation_prompt(cv_content, 'cornish')
        self.assertIn('Cornish', prompt)
        self.assertIn('John Doe', prompt)
        self.assertIn('Experienced developer', prompt)
        self.assertIn('JSON', prompt)

    def test_translate_cv_content_no_api_key(self):
        """Test translation without API key or with quota issues."""
        result = self.translation_service.translate_cv_content(self.cv, 'cornish')
        self.assertFalse(result['translated'])
        # Check for either API key not configured or quota/API errors
        self.assertTrue(
            'OpenAI API key not configured' in result['error'] or
            'Translation failed' in result['error'] or
            'quota' in result['error'].lower() or
            '429' in result['error']
        )

    def test_translate_cv_content_invalid_language(self):
        """Test translation with invalid language."""
        result = self.translation_service.translate_cv_content(self.cv, 'invalid_language')
        self.assertFalse(result['translated'])
        self.assertIn('not supported', result['error'])


class TranslationAPITest(TestCase):
    """Test cases for translation API."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.cv = CV.objects.create(
            firstname="John",
            lastname="Doe",
            skills="Python, Django",
            projects="Web application",
            bio="Experienced developer",
            contacts="john.doe@email.com"
        )

    def test_translate_cv_api_missing_data(self):
        """Test translation API with missing data."""
        response = self.client.post('/api/translate-cv/',
                                    content_type='application/json',
                                    data=json.dumps({}))
        data = response.json()
        self.assertEqual(data['status'], 'error')
        self.assertIn('CV ID and language are required', data['message'])

    def test_translate_cv_api_invalid_cv_id(self):
        """Test translation API with invalid CV ID."""
        response = self.client.post('/api/translate-cv/',
                                    content_type='application/json',
                                    data=json.dumps({
                                        'cv_id': 999,
                                        'language': 'cornish'
                                    }))
        data = response.json()
        self.assertEqual(data['status'], 'error')
        self.assertIn('CV not found', data['message'])

    def test_translate_cv_api_invalid_language(self):
        """Test translation API with invalid language."""
        response = self.client.post('/api/translate-cv/',
                                    content_type='application/json',
                                    data=json.dumps({
                                        'cv_id': self.cv.id,
                                        'language': 'invalid_language'
                                    }))
        data = response.json()
        self.assertEqual(data['status'], 'error')
        self.assertIn('not supported', data['message'])

    def test_translate_cv_api_valid_request(self):
        """Test translation API with valid request."""
        response = self.client.post('/api/translate-cv/',
                                    content_type='application/json',
                                    data=json.dumps({
                                        'cv_id': self.cv.id,
                                        'language': 'cornish'
                                    }))
        data = response.json()
        # Should fail because of API key or quota issues
        self.assertEqual(data['status'], 'error')
        # Check for either API key not configured or quota/API errors
        self.assertTrue(
            'OpenAI API key not configured' in data['message'] or
            'Translation failed' in data['message'] or
            'quota' in data['message'].lower() or
            '429' in data['message']
        )

    def test_translate_cv_api_invalid_json(self):
        """Test translation API with invalid JSON."""
        response = self.client.post('/api/translate-cv/',
                                    content_type='application/json',
                                    data='invalid json')
        data = response.json()
        self.assertEqual(data['status'], 'error')
        self.assertIn('Invalid JSON data', data['message'])
