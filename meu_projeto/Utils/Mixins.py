class BaseGroupRequiredMixin:
    """
    Mixin base para verificação de grupo de usuário.
    """

    allowed_groups = []

    def test_func(self, request):
        """
        Verifica se o usuário pertence a um dos grupos permitidos.
        """
        user_groups = [group.name for group in request.user.groups.all()]
        return any(group in self.allowed_groups for group in user_groups)

class AdminRequiredMixin(BaseGroupRequiredMixin):
    allowed_groups = ['Admins']

class Grupo_de_acesso_3Mixin(BaseGroupRequiredMixin):
    allowed_groups = ['Gestor da empresa', 'Admins']

class Grupo_de_acesso_2Mixin(BaseGroupRequiredMixin):
    allowed_groups = ['Gestor da empresa', 'Operador de dados', 'Admins']

class Grupo_de_acesso_1Mixin(BaseGroupRequiredMixin):
    allowed_groups = ['Gestor da empresa', 'Operador de dados', 'Espectador', 'Admins']
