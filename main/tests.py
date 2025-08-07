from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import CV


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
