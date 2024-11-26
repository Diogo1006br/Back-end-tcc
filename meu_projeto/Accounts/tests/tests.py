from django.test import TestCase
from django.contrib.auth import get_user_model
from Accounts.models import Company_DBTable, CustomUser_DBTable


class UserModelTest(TestCase):
    
    def setUp(self):
        # Criação de uma empresa para associar ao usuário
        self.company = Company_DBTable.objects.create(
            companyName="Test Company",
            CNPJ="12.345.678/0001-90",
            address="Rua Teste, 123",
            city="Cidade Teste",
            state="São Paulo"
        )
    
    def test_create_user(self):
        """Testa a criação de um usuário"""
        user = CustomUser_DBTable.objects.create_user(
            email="user@test.com",
            password="testpassword123",
            firstName="Test",
            companyId=self.company.id  # Passando apenas o ID da empresa
        )

        self.assertEqual(user.email, "user@test.com")
        self.assertTrue(user.check_password("testpassword123"))
        self.assertEqual(user.companyId.id, self.company.id)  # Verifica se o ID está correto
        self.assertEqual(user.firstName, "Test")

    def test_create_superuser(self):
        """Testa a criação de um superusuário"""
        superuser = CustomUser_DBTable.objects.create_superuser(
            email="superuser@test.com",
            password="testpassword123",
            firstName="Admin",
            companyId=self.company.id  # Passando apenas o ID da empresa
        )

        self.assertEqual(superuser.email, "superuser@test.com")
        self.assertTrue(superuser.check_password("testpassword123"))
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

    def test_create_user_without_company(self):
        """Testa a criação de um usuário sem associar a empresa"""
        with self.assertRaises(TypeError):
            CustomUser_DBTable.objects.create_user(
                email="no_company@test.com",
                password="testpassword123",
                firstName="Test"
            )

    def test_user_str_method(self):
        """Testa o método __str__ do usuário"""
        user = CustomUser_DBTable.objects.create_user(
            email="user@test.com",
            password="testpassword123",
            firstName="Test",
            companyId=self.company.id  # Passando o ID da empresa
        )
        self.assertEqual(str(user), "user@test.com")
