from rest_framework.test import APITestCase, APIClient
from rest_framework import status
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
            city="Test City",
            state="SP"
        )

        # Criar um usuário
        self.user = CustomUser_DBTable.objects.create_user(
            email="testuser@test.com",
            password="testpassword",
            companyId=self.company.id
        )
        self.client.force_authenticate(user=self.user)

        # Criar projetos e associar ao usuário autenticado
        self.project1 = Project_DBTable.objects.create(
            projectName="Project 1",
            projectDescription="Description 1",
            owner=self.company
        )
        self.project2 = Project_DBTable.objects.create(
            projectName="Project 2",
            projectDescription="Description 2",
            owner=self.company
        )
        self.project1.members.add(self.user)
        self.project2.members.add(self.user)

        # Ajustar `created_at` para garantir a ordem
        self.project1.created_at = datetime.now() - timedelta(days=2)
        self.project2.created_at = datetime.now()
        self.project1.save()
        self.project2.save()

    def test_project_numbers(self):
        """
        Testa se o número correto de projetos é retornado para o usuário autenticado.
        """
        response = self.client.get('/project_numbers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['project_numbers'], 2)

    def test_recent_projects(self):
        """
        Testa se os projetos recentes são retornados.
        """
        response = self.client.get('/recent_projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['recent_projects']), 2)
        self.assertEqual(response.data['recent_projects'][0]['name'], "Project 2")
        self.assertEqual(response.data['recent_projects'][1]['name'], "Project 1")

    def test_change_project_status(self):
        """
        Testa se o status do projeto pode ser atualizado.
        """
        response = self.client.patch(f'/change_project_status/{self.project1.id}/', data={'status': 'Completed'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'Completed')

    def test_change_project_status_invalid(self):
        """
        Testa se um erro é retornado para um ID de projeto ou status inválido.
        """
        # ID inexistente
        response = self.client.patch('/change_project_status/999/', data={'status': 'InvalidStatus'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Status inválido
        response = self.client.patch(f'/change_project_status/{self.project1.id}/', data={'status': 'InvalidStatus'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
