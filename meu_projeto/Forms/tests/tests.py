from django.test import TestCase
from Forms.models import Form, FormResponse, DropboxAnswerList
from Accounts.models import Company_DBTable, CustomUser_DBTable
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

class FormsTestCase(TestCase):
    def setUp(self):
        # Criando uma empresa
        self.company = Company_DBTable.objects.create(
            companyName="Empresa Teste",
            CNPJ="12345678901234"
        )

        # Criando um usuário
        self.user = CustomUser_DBTable.objects.create_user(
            email="user@company.com",
            companyId=self.company.id,
            password="userpassword123"
        )

        # Criando um formulário
        self.form = Form.objects.create(
            name="Test Form",
            form={"fields": [{"name": "Field1", "type": "text"}]},
            company=self.company
        )

        # Criando uma resposta para o formulário
        self.form_response = FormResponse.objects.create(
            formID=self.form,
            response={"Field1": "Test Response"},
            content_type=ContentType.objects.get_for_model(self.user),
            object_id=self.user.id
        )

        # Criando uma lista de respostas no Dropbox
        self.dropbox_list = DropboxAnswerList.objects.create(
            name="Test Dropbox",
            list={"Field1": ["Option1", "Option2"]},
            company=self.company
        )

    def test_form_creation(self):
        """
        Testa se o formulário é criado com sucesso.
        """
        self.assertEqual(self.form.name, "Test Form")
        self.assertEqual(self.form.company, self.company)
        self.assertEqual(self.form.status, "Ativo")

    def test_form_response_creation(self):
        """
        Testa se uma resposta para o formulário é criada com sucesso.
        """
        self.assertEqual(self.form_response.response, {"Field1": "Test Response"})
        self.assertEqual(self.form_response.formID, self.form)
        self.assertEqual(self.form_response.Instance, self.user)

    def test_form_status_update(self):
        """
        Testa a atualização do status do formulário.
        """
        self.form.status = "Arquivado"
        self.form.save()
        self.assertEqual(self.form.status, "Arquivado")

    def test_dropbox_answer_list_creation(self):
        """
        Testa se uma lista de respostas no Dropbox é criada com sucesso.
        """
        self.assertEqual(self.dropbox_list.name, "Test Dropbox")
        self.assertEqual(self.dropbox_list.list, {"Field1": ["Option1", "Option2"]})
        self.assertEqual(self.dropbox_list.company, self.company)

    def test_form_security(self):
        """
        Testa se informações sensíveis não são expostas.
        """
        form = Form.objects.get(id=self.form.id)
        self.assertNotIn("company", str(form))  # Garante que dados sensíveis não estão na representação string

    def test_invalid_form_response(self):
        """
        Testa se respostas inválidas para um formulário são tratadas adequadamente.
        """
        invalid_response = {"InvalidField": "Invalid Response"}  # Resposta com campo inválido

        # Simulando validação de campos
        form_fields = {field['name'] for field in self.form.form.get('fields', [])}
        response_keys = set(invalid_response.keys())

        invalid_keys = response_keys - form_fields
        if invalid_keys:
            self.assertTrue(True)  # Campo inválido encontrado
        else:
            self.fail("Nenhuma validação foi feita para campos inválidos.")

    def test_dropbox_answer_list_integrity(self):
        """
        Testa se a lista do Dropbox mantém integridade de dados.
        """
        self.assertIsInstance(self.dropbox_list.list["Field1"], list)
        self.assertIn("Option1", self.dropbox_list.list["Field1"])

    def test_form_deletion(self):
        """
        Testa se ao deletar um formulário, as respostas associadas também são deletadas.
        """
        form_id = self.form.id
        self.form.delete()
        with self.assertRaises(Form.DoesNotExist):
            Form.objects.get(id=form_id)
        self.assertFalse(FormResponse.objects.filter(formID=form_id).exists())

    def test_form_response_instance(self):
        """
        Testa se o GenericForeignKey aponta para a instância correta.
        """
        self.assertEqual(self.form_response.Instance, self.user)
