from django.core.management.base import BaseCommand
from Accounts.models import Company_DBTable, CustomUser_DBTable, Plans_DBTable

class Command(BaseCommand):
    """
    Custom command class for creating a new company.

    This class is used to create a new company in the database. It inherits from Django's BaseCommand.

    :param BaseCommand: Base class for management commands.
    :type BaseCommand: django.core.management.base.BaseCommand

    :ivar help: A string that contains a brief description of what the command does.
    :vartype help: str

    Methods
    -------
    add_arguments(self, parser)
        Adds custom arguments to the command parser.

    handle(self, *args, **kwargs)
        Handles the main logic of the command.
    """

    help = 'Create a new company'

    def add_arguments(self, parser):
        """
        Adds custom arguments to the command parser.

        :param parser: The command argument parser.
        :type parser: argparse.ArgumentParser
        """
        parser.add_argument('companyName', type=str, help='Company Name')
        parser.add_argument('CNPJ', type=str, help='Company CNPJ')
        # Add more arguments as needed

    def handle(self, *args, **kwargs):
        """
        Handles the main logic of the command.

        This method creates a new company with the provided name and CNPJ and saves it to the database.

        :param args: Positional arguments.
        :type args: tuple
        :param kwargs: Keyword arguments.
        :type kwargs: dict
        """
        companyName = kwargs['companyName']
        CNPJ = kwargs['CNPJ']
        # Get more arguments as needed

        company = Company_DBTable(companyName=companyName, CNPJ=CNPJ)
        company.save()

        self.stdout.write(self.style.SUCCESS('Company "%s" successfully created!' % companyName))