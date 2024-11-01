from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from rest_framework.response import Response
from rest_framework import status

class BaseGroupRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Classe base para verificar se um usuário pertence a um grupo específico.
    """
    allowed_groups = []  # Lista de grupos permitidos, deve ser definida nas subclasses

    def test_func(self, request=None):
        # Use o request passado como argumento, ou o da instância se disponível
        user = request.user if request else self.request.user
        return any(user.groups.filter(name=group_name).exists() for group_name in self.allowed_groups)

    def handle_no_permission(self):
        # Personalize a resposta de erro aqui
        return Response(status=status.HTTP_403_FORBIDDEN)

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

class Grupo_de_acesso_1Mixin(BaseGroupRequiredMixin):
    """
    Mixin personalizado para verificar se um usuário pertence a um dos grupos permitidos.
    """
    allowed_groups = ['Gestor da empresa', 'Operador de dados', 'Espectador', 'Admins']
