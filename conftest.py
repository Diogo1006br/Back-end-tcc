import os
import django
from pytest_django.lazy_django import skip_if_no_django

# Configure o módulo de configurações do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "/meu_projeto/TCC_API/settings")

# Inicialize o Django
skip_if_no_django()
django.setup()
