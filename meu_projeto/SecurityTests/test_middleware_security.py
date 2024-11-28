from django.test import TestCase, RequestFactory, override_settings
from MiddleWare.TokenMiddleware import CookieTokenMiddleware
from django.http import HttpResponse
from django.urls import path
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TCC_API.settings')

# URLs simuladas para o teste
urlpatterns = [
    path('token_obtain_pair/', lambda request: HttpResponse("Token Obtido"), name='token_obtain_pair'),
    path('is_authenticated/', lambda request: HttpResponse("Usuário autenticado"), name='is_authenticated'),
    path('some-url/', lambda request: HttpResponse("URL para testes"), name='some_url'),
]

@override_settings(ROOT_URLCONF=__name__)  # Aponta para este módulo como configuração de URLs
class MiddlewareSecurityTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = CookieTokenMiddleware(get_response=self.get_response)

    def get_response(self, request):
        return HttpResponse("Middleware funcionando")

    def test_token_in_header(self):
        # Simula uma requisição com um token no cookie
        request = self.factory.get('/some-url/')
        request.COOKIES['access_token'] = 'test_token'
        response = self.middleware(request)
        
        # Valida que o token foi adicionado ao cabeçalho HTTP_AUTHORIZATION
        self.assertEqual(
            request.META.get('HTTP_AUTHORIZATION'), 'Bearer test_token'
        )
        self.assertEqual(response.status_code, 200)

    def test_no_token(self):
        # Simula uma requisição sem um token no cookie
        request = self.factory.get('/some-url/')
        response = self.middleware(request)
        
        # Valida que o cabeçalho HTTP_AUTHORIZATION não foi adicionado
        self.assertIsNone(request.META.get('HTTP_AUTHORIZATION'))
        self.assertEqual(response.status_code, 200)

    def test_skip_urls(self):
        # Simula uma requisição para uma URL que deve ser ignorada pelo middleware
        request = self.factory.get('/token_obtain_pair/')
        response = self.middleware(request)
        
        # Valida que o cabeçalho HTTP_AUTHORIZATION não foi adicionado
        self.assertIsNone(request.META.get('HTTP_AUTHORIZATION'))
        self.assertEqual(response.status_code, 200)
