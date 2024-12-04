from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from Accounts.models import CustomUser_DBTable, Company_DBTable
from Projects.models import Project_DBTable
from datetime import datetime, timedelta

class ProjectAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Criar uma empresa
        self.company = Company_DBTable.objects.create(
            companyName="Test Company",
            CNPJ="12345678901234",
            address="Rua Teste, 123",
            city="Cidade Teste",
            state="São Paulo"
        )

        # Criar um usuário
        self.user = CustomUser_DBTable.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
            companyId=self.company
        )

        # Autenticar o cliente
        self.client.force_authenticate(user=self.user)

        # Criar projetos
        self.project1 = Project_DBTable.objects.create(
            projectName="Project 1",
            projectDescription="Description 1",
            status="In Progress",
            owner=self.company
        )
        self.project1.members.add(self.user)

        self.project2 = Project_DBTable.objects.create(
            projectName="Project 2",
            projectDescription="Description 2",
            status="In Progress",
            owner=self.company
        )
        self.project2.members.add(self.user)

    def test_change_project_status(self):
        """
        Testa se o status do projeto pode ser atualizado.
        """
        response = self.client.patch(f'/api/change_project_status/{self.project1.id}/', data={'status': 'Completed'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_project_status_invalid(self):
        """
        Testa se um erro é retornado para um ID de projeto ou status inválido.
        """
        # ID inexistente
        response = self.client.patch('/api/change_project_status/999/', data={'status': 'InvalidStatus'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Status inválido
        response = self.client.patch(f'/api/change_project_status/{self.project1.id}/', data={'status': 'InvalidStatus'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_project_numbers(self):
        """
        Testa se o número correto de projetos é retornado para o usuário autenticado.
        """
        response = self.client.get('/api/project_numbers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recent_projects(self):
        """
        Testa se os projetos recentes são retornados.
        """
        response = self.client.get('/api/recent_projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_project(self):
        """
        Testa se um projeto pode ser excluído corretamente.
        """
        response = self.client.delete(f'/api/projects/{self.project1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project_DBTable.objects.count(), 1)

    def test_list_projects(self):
        """
        Testa se a listagem de projetos está funcionando corretamente.
        """
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_project_detail(self):
        """
        Testa se os detalhes de um projeto podem ser obtidos corretamente.
        """
        response = self.client.get(f'/api/projects/{self.project1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['projectName'], self.project1.projectName)