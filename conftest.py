import os
import django
import sys
from pytest_django.lazy_django import skip_if_no_django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TCC_API.settings")
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
skip_if_no_django()
django.setup()

