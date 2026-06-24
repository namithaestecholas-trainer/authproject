from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthSystemTests(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.email = "testuser@example.com"
        self.password = "Secur3P@ssw0rd!"
        # Create a user for login and duplicate checks
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

    def test_anonymous_root_redirects_to_login(self):
        """
        An unauthenticated request to root '/' redirects to login.
        """
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('login'))

    def test_authenticated_root_redirects_to_dashboard(self):
        """
        An authenticated request to root '/' redirects to dashboard.
        """
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_anonymous_dashboard_access_denied(self):
        """
        An unauthenticated request to dashboard redirects to login.
        """
        response = self.client.get(reverse('dashboard'))
        # django login_required decorator redirects to LOGIN_URL with next parameter
        expected_url = f"{reverse('login')}?next={reverse('dashboard')}"
        self.assertRedirects(response, expected_url)

    def test_authenticated_dashboard_access_allowed(self):
        """
        An authenticated request can access the dashboard.
        """
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertContains(response, f"Welcome, {self.username}")

    def test_registration_validation_duplicate_email(self):
        """
        Registering with an already registered email address is prevented.
        """
        # Attempt to register with a new username but the same email
        data = {
            'username': 'newuser',
            'email': self.email,  # already registered in setUp
            'password': 'NewPassword123!',
            'confirm_password': 'NewPassword123!'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'email', "A user with this email address already exists.")

    def test_registration_validation_password_mismatch(self):
        """
        Registering with mismatched password and confirm_password yields a validation error.
        """
        data = {
            'username': 'anotheruser',
            'email': 'another@example.com',
            'password': 'PasswordOne1!',
            'confirm_password': 'PasswordTwo2!'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'confirm_password', "Passwords do not match.")

    def test_successful_registration(self):
        """
        Registering with valid unique credentials creates a user, logs them in, and redirects to dashboard.
        """
        data = {
            'username': 'registereduser',
            'email': 'registered@example.com',
            'password': 'UniquePassWord123!',
            'confirm_password': 'UniquePassWord123!'
        }
        response = self.client.post(reverse('register'), data)
        self.assertRedirects(response, reverse('dashboard'))
        
        # Verify user is created in database
        self.assertTrue(User.objects.filter(username='registereduser').exists())
