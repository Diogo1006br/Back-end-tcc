from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.mixins import AccessMixin

class BaseGroupRequiredMixin:
    allowed_groups = []  # Lista de grupos permitidos, a ser definida nas subclasses

    def test_func(self):
        # Obtém os nomes dos grupos do usuário
        user_groups = [group.name for group in self.request.user.groups.all()]
        # Verifica se algum grupo do usuário está nos grupos permitidos
        allowed = any(group in self.allowed_groups for group in user_groups)
        
        # Logs para debug
        print(f"Grupos do usuário: {user_groups}")
        print(f"Grupos permitidos: {self.allowed_groups}")
        print(f"Acesso permitido: {allowed}")  # Log para diagnosticar o retorno
        
        return allowed

    def handle_no_permission(self):
        # Este método trata o caso onde o acesso é negado
        return Response({'detail': 'Access denied'}, status=403)

class AdminRequiredMixin(BaseGroupRequiredMixin):
    """
    Mixin personalizado para verificar se um usuário pertence ao grupo 'Admins'.
    """
    allowed_groups = ['Admins']

class Grupo_de_acesso_3Mixin(BaseGroupRequiredMixin):
    """
    Mixin personalizado para verificar se um usuário pertence a um dos grupos permitidos.
    """
    allowed_groups = ['Gestor da empresa', 'Admins']

class Grupo_de_acesso_2Mixin(BaseGroupRequiredMixin):
    """
    Mixin personalizado para verificar se um usuário pertence a um dos grupos permitidos.
    """
    allowed_groups = ['Gestor da empresa', 'Operador de dados', 'Admins']

class Grupo_de_acesso_1Mixin(AccessMixin):
    """
    Mixin personalizado para verificar se um usuário pertence a um dos grupos permitidos.
    """
    allowed_groups = ['Gestor da empresa', 'Operador de dados', 'Espectador', 'Admins']

    def test_func(self):
        # Verifica se o usuário está autenticado e pertence a algum dos grupos permitidos
        if self.request.user.is_authenticated:
            user_groups = self.request.user.groups.values_list('name', flat=True)
            return any(group in user_groups for group in self.allowed_groups)
        return False

    def handle_no_permission(self):
        # Retorna uma resposta de erro caso o usuário não tenha permissão
        return Response({'detail': 'Permissão negada'}, status=status.HTTP_403_FORBIDDEN)
