from django.core.management.base import BaseCommand
from Accounts.models import Company_DBTable

class Command(BaseCommand):
    help = 'Create a new company'

    def add_arguments(self, parser):
        parser.add_argument('companyName', type=str, help='Nome da empresa')
        parser.add_argument('CNPJ', type=str, help='CNPJ da empresa')

    def handle(self, *args, **kwargs):
        companyName = kwargs['companyName']
        CNPJ = kwargs['CNPJ']
        company = Company_DBTable.objects.create(companyName=companyName, CNPJ=CNPJ)
        self.stdout.write(self.style.SUCCESS(f'Empresa "{companyName}" criada com sucesso!'))
