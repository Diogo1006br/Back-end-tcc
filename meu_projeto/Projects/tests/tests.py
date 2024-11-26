from django.test import TestCase
from Accounts.models import User, Company_DBTable  # Importando os modelos necessários
from Projects.models import Project  # Assumindo que você tenha o modelo de Project

class ProjectViewSetTestCase(TestCase):
    def setUp(self):
        # Criando uma instância de empresa de exemplo
        self.company = Company_DBTable.objects.create(
            name='Test Company'
        )

        # Criando um usuário com o ID da empresa, não o objeto inteiro
        self.user = User.objects.create_user(
            email='testuser@teste.com', 
            password='testpass', 
            companyId=self.company.id  # Passando o ID da empresa
        )

        # Criando um projeto associado à empresa (usando companyId)
        self.project = Project.objects.create(
            name="Test Project",
            description="Project description",
            company=self.company,  # Referência direta ao modelo Company_DBTable
            owner=self.user
        )

    def test_create_project(self):
        """
        Testa a criação de um novo projeto
        """
        response = self.client.post('/create_project/', {
            'name': 'New Project',
            'description': 'Project description',
            'companyId': self.company.id  # Passando o ID da empresa corretamente
        })
        self.assertEqual(response.status_code, 201)
        self.assertContains(response, 'Project created successfully')

    def test_change_project_status(self):
        """
        Testa a mudança de status de um projeto
        """
        response = self.client.patch(f'/projects/{self.project.id}/change_status/', {
            'new_status': 'completed'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Status updated successfully')

    def test_invalid_status_change(self):
        """
        Testa tentativa de mudar para um status inválido
        """
        response = self.client.patch(f'/projects/{self.project.id}/change_status/', {
            'new_status': 'invalid_status'
        })
        self.assertEqual(response.status_code, 400)  # Bad Request
        self.assertContains(response, 'Invalid status')

    def test_create_project_with_invalid_data(self):
        """
        Testa a criação de projeto com dados inválidos
        """
        response = self.client.post('/create_project/', {
            'name': '',  # Nome do projeto está faltando
            'description': 'Description without name',
            'companyId': self.company.id  # Passando o ID correto da empresa
        })
        self.assertEqual(response.status_code, 400)  # Espera um erro por dados inválidos
        self.assertContains(response, 'This field is required')

    def test_logout(self):
        """
        Testa o logout com token válido
        """
        # Autenticando o usuário
        self.client.login(email='testuser@teste.com', password='testpass')
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'logged out')

    def test_logout_without_token(self):
        """
        Testa o logout sem passar token
        """
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, 401)  # Unauthorized
        self.assertContains(response, 'Token is missing or invalid')

    def test_token_refresh(self):
        """
        Testa o refresh de token com um token válido
        """
        self.client.login(email='testuser@teste.com', password='testpass')
        response = self.client.post('/refresh_token/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'token refreshed')

    def test_token_refresh_invalid(self):
        """
        Testa o refresh de token com um token inválido
        """
        response = self.client.post('/refresh_token/', {
            'token': 'invalidtoken'
        })
        self.assertEqual(response.status_code, 401)  # Unauthorized
        self.assertContains(response, 'Invalid token')

    def test_authenticate_valid_user(self):
        """
        Testa o login com credenciais válidas
        """
        response = self.client.post('/login/', {
            'email': 'testuser@teste.com',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'login successful')

    def test_authenticate_invalid_user(self):
        """
        Testa o login com credenciais inválidas
        """
        response = self.client.post('/login/', {
            'email': 'invaliduser@teste.com',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Invalid credentials')
