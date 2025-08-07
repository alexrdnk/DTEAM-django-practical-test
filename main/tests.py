from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import CV


class CVModelTest(TestCase):
    """Test cases for the CV model."""

    def setUp(self):
        """Set up test data."""
        self.cv = CV.objects.create(
            firstname="John",
            lastname="Doe",
            skills="Python, Django, JavaScript",
            projects="E-commerce Platform: Built a full-stack application",
            bio="Experienced Full-Stack Developer with 5+ years of experience",
            contacts="Email: john.doe@example.com\nPhone: +1 (555) 123-4567"
        )

    def test_cv_creation(self):
        """Test that a CV can be created."""
        self.assertEqual(self.cv.firstname, "John")
        self.assertEqual(self.cv.lastname, "Doe")
        self.assertEqual(self.cv.skills, "Python, Django, JavaScript")

    def test_cv_str_method(self):
        """Test the string representation of CV."""
        self.assertEqual(str(self.cv), "John Doe")

    def test_cv_get_full_name(self):
        """Test the get_full_name method."""
        self.assertEqual(self.cv.get_full_name(), "John Doe")

    def test_cv_ordering(self):
        """Test that CVs are ordered by creation date."""
        cv2 = CV.objects.create(
            firstname="Jane",
            lastname="Smith",
            skills="React, Node.js",
            projects="Task Management App",
            bio="Frontend Developer",
            contacts="Email: jane.smith@example.com"
        )
        cvs = list(CV.objects.all())
        self.assertEqual(cvs[0], cv2)  # Newer CV should be first


class CVListViewTest(TestCase):
    """Test cases for the CV list view."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.cv1 = CV.objects.create(
            firstname="John",
            lastname="Doe",
            skills="Python, Django",
            projects="E-commerce Platform",
            bio="Full-Stack Developer",
            contacts="Email: john.doe@example.com"
        )
        self.cv2 = CV.objects.create(
            firstname="Jane",
            lastname="Smith",
            skills="React, Node.js",
            projects="Task Management App",
            bio="Frontend Developer",
            contacts="Email: jane.smith@example.com"
        )

    def test_cv_list_view_status_code(self):
        """Test that the CV list view returns 200 status code."""
        response = self.client.get(reverse('main:cv_list'))
        self.assertEqual(response.status_code, 200)

    def test_cv_list_view_template(self):
        """Test that the CV list view uses the correct template."""
        response = self.client.get(reverse('main:cv_list'))
        self.assertTemplateUsed(response, 'main/cv_list.html')

    def test_cv_list_view_context(self):
        """Test that the CV list view has the correct context."""
        response = self.client.get(reverse('main:cv_list'))
        self.assertIn('cvs', response.context)
        self.assertEqual(len(response.context['cvs']), 2)

    def test_cv_list_view_ordering(self):
        """Test that CVs are ordered by creation date (newest first)."""
        response = self.client.get(reverse('main:cv_list'))
        cvs = response.context['cvs']
        self.assertEqual(cvs[0], self.cv2)  # Newer CV should be first
        self.assertEqual(cvs[1], self.cv1)  # Older CV should be second


class CVDetailViewTest(TestCase):
    """Test cases for the CV detail view."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.cv = CV.objects.create(
            firstname="John",
            lastname="Doe",
            skills="Python, Django, JavaScript",
            projects="E-commerce Platform: Built a full-stack application",
            bio="Experienced Full-Stack Developer with 5+ years of experience",
            contacts="Email: john.doe@example.com\nPhone: +1 (555) 123-4567"
        )

    def test_cv_detail_view_status_code(self):
        """Test that the CV detail view returns 200 status code."""
        response = self.client.get(reverse('main:cv_detail', kwargs={'pk': self.cv.pk}))
        self.assertEqual(response.status_code, 200)

    def test_cv_detail_view_template(self):
        """Test that the CV detail view uses the correct template."""
        response = self.client.get(reverse('main:cv_detail', kwargs={'pk': self.cv.pk}))
        self.assertTemplateUsed(response, 'main/cv_detail.html')

    def test_cv_detail_view_context(self):
        """Test that the CV detail view has the correct context."""
        response = self.client.get(reverse('main:cv_detail', kwargs={'pk': self.cv.pk}))
        self.assertIn('cv', response.context)
        self.assertEqual(response.context['cv'], self.cv)

    def test_cv_detail_view_404(self):
        """Test that the CV detail view returns 404 for non-existent CV."""
        response = self.client.get(reverse('main:cv_detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)


class CVAdminTest(TestCase):
    """Test cases for the CV admin interface."""

    def setUp(self):
        """Set up test data."""
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.client = Client()
        self.client.login(username='admin', password='adminpass123')

    def test_admin_cv_list_view(self):
        """Test that CVs are visible in admin interface."""
        cv = CV.objects.create(
            firstname="John",
            lastname="Doe",
            skills="Python, Django",
            projects="E-commerce Platform",
            bio="Full-Stack Developer",
            contacts="Email: john.doe@example.com"
        )
        response = self.client.get('/admin/main/cv/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")
