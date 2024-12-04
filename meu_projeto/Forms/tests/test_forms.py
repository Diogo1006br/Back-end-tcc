from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from Accounts.models import Company_DBTable, CustomUser_DBTable
from Forms.models import Form

class FormsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Criando uma empresa
        self.company = Company_DBTable.objects.create(
            companyName="Empresa Teste",
            CNPJ="12345678901234",
            address="Rua Teste, 123",
            city="Cidade Teste",
            state="São Paulo"
        )

        # Criando um usuário
        self.user = CustomUser_DBTable.objects.create_user(
            username="user",
            email="user@company.com",
            companyId=self.company,
            password="userpassword123"
        )

        # Criando um formulário fictício
        self.form = Form.objects.create(
            name="Formulário Teste",
            form={"field": "value"},
            company=self.company
        )

    def test_form_creation(self):
        """Testa a criação de um formulário."""
        self.assertEqual(self.form.name, "Formulário Teste")
        self.assertEqual(self.form.company, self.company)

    def test_form_deletion(self):
        """Testa a exclusão de um formulário."""
        self.form.delete()
        self.assertFalse(Form.objects.filter(id=self.form.id).exists())

    def test_invalid_form_response(self):
        """Testa a resposta inválida de um formulário."""
        response = self.client.post('/api/forms/', {
            'name': '',
            'form': {"field": "value"},
            'company': self.company.id
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_form_detail(self):
        """Testa a obtenção dos detalhes de um formulário."""
        response = self.client.get(f'/api/forms/{self.form.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.form.name)

    def test_form_update_name(self):
        """Testa a atualização do nome de um formulário."""
        response = self.client.patch(f'/api/forms/{self.form.id}/', {
            'name': 'Formulário Atualizado'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.form.refresh_from_db()
        self.assertEqual(self.form.name, 'Formulário Atualizado')

    def test_form_list(self):
        """Testa a listagem de formulários."""
        response = self.client.get('/api/forms/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 0)

    def test_form_list_empty(self):
        """Testa a listagem de formulários quando não há formulários."""
        Form.objects.all().delete()
        response = self.client.get('/api/forms/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)