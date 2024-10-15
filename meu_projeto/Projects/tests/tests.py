from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from Projects.models import Project_DBTable
from Accounts.models import Company_DBTable
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()
class ProjectViewSetTestCase(APITestCase):
    """
    Test case for the Project view set.

    This class contains unit tests for the Project view set. It inherits from Django Rest Framework's APITestCase.

    :param APITestCase: Base class for creating API test cases.
    :type APITestCase: rest_framework.test.APITestCase

    Methods
    -------
    setUp(self)
        Sets up the test environment before each test method is run.

    test_list_projects(self)
        Tests the list projects endpoint.

    test_create_project(self)
        Tests the create project endpoint.

    test_update_project(self)
        Tests the update project endpoint.

    test_create_project_with_invalid_member(self)
        Tests the create project endpoint with an invalid member.

    test_update_project_with_invalid_member(self)
        Tests the update project endpoint with an invalid member.

    test_create_project_without_members(self)
        Tests the create project endpoint without members.

    test_update_project_without_members(self)
        Tests the update project endpoint without members.

    test_create_project_without_authentication(self)
        Tests the create project endpoint without authentication.

    test_update_project_without_authentication(self)
        Tests the update project endpoint without authentication.

    test_create_project_with_invalid_data(self)
        Tests the create project endpoint with invalid data.

    test_update_project_with_invalid_data(self)
        Tests the update project endpoint with invalid data.

    tearDown(self)
        Cleans up the test environment after each test method has run.
    """
    def setUp(self):
        """
        Sets up the test environment before each test method is run.

        This method creates a test client, a test company, a test user, a test project, and a test token.
        """
        # Implementation...
        self.client = APIClient()
        self.company = Company_DBTable.objects.create(company_name='Test Company', CNPJ='12345678901234')
        self.user = User.objects.create(email='testuser@teste.com', password='testpass',company_id=self.company)
        self.client.login(email='testuser@teste.com', password='testpass')
        self.project = Project_DBTable.objects.create(project_name='Test Project', project_description='Test Description', owner=self.user.company_id)
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')

    def test_list_projects(self):
        """
        Tests the list projects endpoint.

        This method sends a GET request to the list projects endpoint and checks the response.
        """
        response = self.client.get('/projects/')
        
        self.assertEqual(response.status_code, 200)

    def test_create_project(self):
        """
        Tests the create project endpoint.

        This method sends a POST request to the create project endpoint and checks the response.
        """
        member= []

        member.append(self.user.email)
        data = {
            "project_name": "New Project",
            "project_description": "New Description",
            "members": member,
            "owner": self.user.company_id.pk
        }
        
        response = self.client.post('/projects/', data=data, format='json')
        
        self.assertEqual(response.status_code, 201)

    def test_update_project(self):
        """
        Tests the update project endpoint.

        This method sends a PUT request to the update project endpoint and checks the response.
        """
        member= []

        member.append(self.user.email)
        data = {
            "project_name": "Updated Project",
            "project_description": "Updated Description",
            "members": member,
            "owner": self.user.company_id.pk
        }
        response = self.client.put(f'/projects/{self.project.id}/', data=data, format='json')
        
        self.assertEqual(response.status_code, 200)

    def test_create_project_with_invalid_member(self):
        """
        Tests the create project endpoint with an invalid member.

        This method sends a POST request to the create project endpoint with an invalid memberand checks the response.
        """
        data = {
            "project_name": "New Project",
            "project_description": "New Description",
            "members": ["invalidemail@example.com"],
            "owner": self.user.company_id.pk
        }
        response = self.client.post('/projects/', data=data, format='json')
        
        self.assertEqual(response.status_code, 400)

    def test_update_project_with_invalid_member(self):
        """
        Tests the update project endpoint with an invalid member.

        This method sends a PUT request to the update project endpoint with an invalid memberand checks the response.
        """
        data = {
            "project_name": "Updated Project",
            "project_description": "Updated Description",
            "members": ["invalidemail@example.com"],
            "owner": self.user.company_id.pk
        }
        response = self.client.put(f'/projects/{self.project.id}/', data=data, format='json')
        
        self.assertEqual(response.status_code, 400)

    def test_create_project_without_members(self):
        """
        Tests the create project endpoint without members.

        This method sends a POST request to the create project endpoint without members and checks the response.
        """
        data = {
            "project_name": "New Project",
            "project_description": "New Description",
            "owner": self.user.company_id.pk
        }
        response = self.client.post('/projects/', data=data, format='json')
        
        self.assertEqual(response.status_code, 400)

    def test_update_project_without_members(self):
        """
        Tests the update project endpoint without members.

        This method sends a PUT request to the update project endpoint without members and checks the response.
        """
        data = {
            "project_name": "Updated Project",
            "project_description": "Updated Description",
            "owner": self.user.company_id.pk
        }
        response = self.client.put(f'/projects/{self.project.id}/', data=data, format='json')
        
        self.assertEqual(response.status_code, 400)

    def test_create_project_without_authentication(self):
        """
        Tests the create project endpoint without authentication.

        This method sends a POST request to the create project endpoint without authentication and checks the response.
        """
        self.client.logout()
        data = {
            "project_name": "New Project",
            "project_description": "New Description",
            "members": [self.user.email],
            "owner": self.user.company_id.pk
        }
        response = self.client.post('/projects/', data=data, format='json')
        
        self.assertEqual(response.status_code, 401)

    def test_update_project_without_authentication(self):
        """
        Tests the update project endpoint without authentication.

        This method sends a PUT request to the update project endpoint without authentication and checks the response.
        """
        self.client.logout()
        data = {
            "project_name": "Updated Project",
            "project_description": "Updated Description",
            "members": [self.user.email],
            "owner": self.user.company_id.pk
        }
        response = self.client.put(f'/projects/{self.project.id}/', data=data, format='json')
        
        self.assertEqual(response.status_code, 401)

    def test_create_project_with_invalid_data(self):
        """
        Tests the create project endpoint with invalid data.

        This method sends a POST request to the create project endpoint with invalid data and checks the response.
        """
        data = {
            "project_name": "",
            "project_description": "New Description",
            "members": [self.user.email],
            "owner": "invalid_owner_id"
        }
        response = self.client.post('/projects/', data=data, format='json')
        
        self.assertEqual(response.status_code, 400)

    def test_update_project_with_invalid_data(self):
        """
        Tests the update project endpoint with invalid data.

        This method sends a PUT request to the update project endpoint with invalid data and checks the response.
        """
        data = {
            "project_name": "",
            "project_description": "Updated Description",
            "members": [self.user.email],
            "owner": "invalid_owner_id"
        }
        response = self.client.put(f'/projects/{self.project.id}/', data=data, format='json')
        
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        """
        Cleans up the test environment after each test method has run.

        This method logs out the test client.
        """
        self.client.logout()