from django.test import TestCase
from Accounts.models import CustomUser_DBTable, Company_DBTable
from Registrations.models import Asset_DBTable, SubItem_DBTable
from Projects.models import Project_DBTable
from Forms.models import Form
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TCC_API.settings')


class RegistrationTests(TestCase):
    def setUp(self):
        # Criar uma empresa
        self.company = Company_DBTable.objects.create(
            companyName="Empresa Teste",
            CNPJ="12345678901234",
        )

        # Criar um usuário
        self.user = CustomUser_DBTable.objects.create_user(
            email="teste@teste.com",
            password="senha123",
            companyId=self.company.id,  # Passar o ID da empresa
        )

        # Criar um projeto
        self.project = Project_DBTable.objects.create(
            projectName="Projeto Teste",
            projectDescription="Descrição do Projeto Teste",
            owner=self.company,
        )
        self.project.members.add(self.user)  # Adicionar usuário como membro do projeto

        # Criar um formulário
        self.form = Form.objects.create(
            name="Formulário Teste",
            form={"campo1": "valor1", "campo2": "valor2"},  # JSONField exemplo
            company=self.company,
            status="Ativo",
        )

        # Criar um ativo
        self.asset = Asset_DBTable.objects.create(
            assetName="Ativo Teste",
            form=self.form,
            project=self.project,  # Vincular ao projeto
            status="Ativo",
            is_ocult=False,
        )

        # Criar um subitem
        self.sub_item = SubItem_DBTable.objects.create(
            elementName="Elemento Teste",
            asset=self.asset,
            form=self.form,
            is_ocult=False,
        )

    def test_asset_creation(self):
        """
        Teste para verificar a criação de um ativo.
        """
        self.assertEqual(self.asset.assetName, "Ativo Teste")
        self.assertEqual(self.asset.form, self.form)
        self.assertEqual(self.asset.project, self.project)
        self.assertFalse(self.asset.is_ocult)

    def test_asset_detail(self):
        """
        Teste para obter detalhes de um ativo.
        """
        asset = Asset_DBTable.objects.get(id=self.asset.id)
        self.assertEqual(asset.assetName, "Ativo Teste")
        self.assertEqual(asset.form, self.form)
        self.assertEqual(asset.project, self.project)

    def test_asset_list(self):
        """
        Teste para listar ativos.
        """
        assets = Asset_DBTable.objects.all()
        self.assertIn(self.asset, assets)

    def test_delete_asset(self):
        """
        Teste para deletar um ativo.
        """
        self.asset.delete()
        assets = Asset_DBTable.objects.all()
        self.assertNotIn(self.asset, assets)

    def test_sub_item_creation(self):
        """
        Teste para criar um subitem.
        """
        self.assertEqual(self.sub_item.elementName, "Elemento Teste")
        self.assertEqual(self.sub_item.asset, self.asset)
        self.assertEqual(self.sub_item.form, self.form)

    def test_update_asset(self):
        """
        Teste para atualizar um ativo.
        """
        self.asset.assetName = "Ativo Atualizado"
        self.asset.save()
        updated_asset = Asset_DBTable.objects.get(id=self.asset.id)
        self.assertEqual(updated_asset.assetName, "Ativo Atualizado")
