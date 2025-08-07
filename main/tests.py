from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import CV, RequestLog
from .context_processors import settings_context


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
