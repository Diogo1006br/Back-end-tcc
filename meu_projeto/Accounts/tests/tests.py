
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from Accounts.models import Company_DBTable
from rest_framework_simplejwt.tokens import RefreshToken

class LoginViewTest(TestCase):
    """
    Test case for the login view.

    This class contains unit tests for the login view. It inherits from Django's TestCase.

    :param TestCase: Base class for creating unit tests.
    :type TestCase: django.test.TestCase

    Methods
    -------
    setUp(self)
        Sets up the test environment before each test method is run.

    test_authenticate_valid_user(self)
        Tests the login view with valid user credentials.

    test_authenticate_invalid_user(self)
        Tests the login view with invalid user credentials.

    test_authenticate_no_credentials(self)
        Tests the login view without any credentials.
    """

    def setUp(self):
        """
        Sets up the test environment before each test method is run.

        This method creates a test client, a test company, a test user, and a test token.
        """
        self.client = APIClient()
        self.company = Company_DBTable.objects.create(company_name='Test Company', CNPJ='12345678901234')
        self.user = get_user_model().objects.create_user(email='test@test.com', password='testpassword', company_id=self.company.pk)
        self.url = reverse('login')
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')

    def test_authenticate_valid_user(self):
        """
        Tests the login view with valid user credentials.

        This method sends a POST request to the login view with valid user credentials and checks the response.
        """
        response = self.client.post(self.url, {'email': 'test@test.com', 'password': 'testpassword'},format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_authenticate_invalid_user(self):
        """
        Tests the login view with invalid user credentials.

        This method sends a POST request to the login view with invalid user credentials and checks the response.
        """
        response = self.client.post(self.url, {'email': 'test@test.com', 'password': 'wrongpassword'},format='json')
        self.assertEqual(response.status_code, 401)

    def test_authenticate_no_credentials(self):
        """
        Tests the login view without any credentials.

        This method sends a POST request to the login view without any credentials and checks the response.
        """
        response = self.client.post(self.url, {},format='json')
        self.assertEqual(response.status_code, 400)
        

# Create your tests here.
