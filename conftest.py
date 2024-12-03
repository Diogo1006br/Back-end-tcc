import os
import django
import sys
from pytest_django.lazy_django import skip_if_no_django

# Adiciona o diretório do projeto ao Python Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "meu_projeto")))

# Configura o módulo de configurações do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TCC_API.settings")

# Inicializa o Django
skip_if_no_django()
django.setup()

