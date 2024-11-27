from django.test import TestCase
from Accounts.models import Company_DBTable  # Certifique-se de ajustar o caminho
from Registrations.models import Asset_DBTable, SubItem_DBTable, Asset_Sub_Element_DBTable
from Forms.models import Form

class RegistrationsModelTests(TestCase):
    def setUp(self):
        # Criando uma empresa fictícia
        self.company = Company_DBTable.objects.create()

        # Criando um formulário fictício
        self.form = Form.objects.create(
            name="Formulário Teste",
            form={"field": "value"},
            company=self.company
        )

        # Criando um ativo fictício
        self.asset = Asset_DBTable.objects.create(
            assetName="Ativo Teste",
            form=self.form,
            company=self.company,
            status="Ativo"
        )

        # Criando um subitem fictício
        self.sub_item = SubItem_DBTable.objects.create(
            elementName="Subitem Teste",
            asset=self.asset,
            form=self.form
        )

    def test_asset_creation(self):
        """Testa se um ativo pode ser criado corretamente."""
        self.assertEqual(self.asset.assetName, "Ativo Teste")
        self.assertEqual(self.asset.form, self.form)
        self.assertEqual(self.asset.status, "Ativo")

    def test_sub_item_creation(self):
        """Testa se um subitem pode ser criado corretamente."""
        self.assertEqual(self.sub_item.elementName, "Subitem Teste")
        self.assertEqual(self.sub_item.asset, self.asset)
        self.assertEqual(self.sub_item.form, self.form)

    def test_asset_deletion(self):
        """Testa a exclusão de um ativo e seus dependentes."""
        self.asset.delete()
        self.assertEqual(SubItem_DBTable.objects.filter(asset=self.asset).count(), 0)

    def test_sub_item_deletion(self):
        """Testa a exclusão de um subitem."""
        self.sub_item.delete()
        self.assertEqual(SubItem_DBTable.objects.filter(pk=self.sub_item.pk).count(), 0)

    def test_asset_list(self):
        """Testa se a listagem de ativos retorna corretamente."""
        assets = Asset_DBTable.objects.all()
        self.assertIn(self.asset, assets)

    def test_sub_item_list(self):
        """Testa se a listagem de subitens retorna corretamente."""
        sub_items = SubItem_DBTable.objects.filter(asset=self.asset)
        self.assertIn(self.sub_item, sub_items)

    def test_sub_element_creation(self):
        """Testa se um subelemento pode ser criado corretamente."""
        sub_element = Asset_Sub_Element_DBTable.objects.create(
            nameSubElement="SubElemento Teste",
            element=self.sub_item,
            form=self.form
        )
        self.assertEqual(sub_element.nameSubElement, "SubElemento Teste")
        self.assertEqual(sub_element.element, self.sub_item)
        self.assertEqual(sub_element.form, self.form)

    def test_sub_element_deletion(self):
        """Testa a exclusão de um subelemento."""
        sub_element = Asset_Sub_Element_DBTable.objects.create(
            nameSubElement="SubElemento Teste",
            element=self.sub_item,
            form=self.form
        )
        sub_element.delete()
        self.assertEqual(Asset_Sub_Element_DBTable.objects.filter(pk=sub_element.pk).count(), 0)

    def test_sub_element_list(self):
        """Testa se a listagem de subelementos retorna corretamente."""
        sub_element = Asset_Sub_Element_DBTable.objects.create(
            nameSubElement="SubElemento Teste",
            element=self.sub_item,
            form=self.form
        )
        sub_elements = Asset_Sub_Element_DBTable.objects.filter(element=self.sub_item)
        self.assertIn(sub_element, sub_elements)
