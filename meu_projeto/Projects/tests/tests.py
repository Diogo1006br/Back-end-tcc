from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
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
            companyId=self.company.id  # Passar o ID, não o objeto
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
        url = reverse('project_numbers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['project_numbers'], 2)

    def test_recent_projects(self):
        """
        Testa se os projetos recentes são retornados.
        """
        url = reverse('recent_projects')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['recent_projects']), 2)
        self.assertEqual(response.data['recent_projects'][0]['name'], "Project 2")
        self.assertEqual(response.data['recent_projects'][1]['name'], "Project 1")

    def test_change_project_status(self):
        """
        Testa se o status do projeto pode ser atualizado.
        """
        url = reverse('change_project_status', args=[self.project1.id])
        response = self.client.patch(url, data={'status': 'Completed'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'Completed')

    def test_change_project_status_invalid(self):
        """
        Testa se um erro é retornado para um ID de projeto ou status inválido.
        """
        # ID inexistente
        invalid_id_url = reverse('change_project_status', args=[999])
        response = self.client.patch(invalid_id_url, data={'status': 'InvalidStatus'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Status inválido
        valid_id_url = reverse('change_project_status', args=[self.project1.id])
        response = self.client.patch(valid_id_url, data={'status': 'InvalidStatus'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
