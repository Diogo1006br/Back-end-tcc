from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from rest_framework.response import Response
from rest_framework import status


class BaseGroupRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
 

    allowed_groups = []  
    def test_func(self,request):

        user = request.user
        return any(user.groups.filter(name=group_name).exists() for group_name in self.allowed_groups)

    def handle_no_permission(self):

        return Response(status=status.HTTP_403_FORBIDDEN)
    
class AdminRequiredMixin(BaseGroupRequiredMixin):
   
    allowed_groups = ['Admins']

class Grupo_de_acesso_3Mixin(BaseGroupRequiredMixin):
 
    allowed_groups = ['Gestor da empresa', 'Admins']

class Grupo_de_acesso_2Mixin(BaseGroupRequiredMixin):
   
    allowed_groups = ['Gestor da empresa', 'Operador de dados', 'Admins']

class Grupo_de_acesso_1Mixin(BaseGroupRequiredMixin):
  
    allowed_groups = ['Gestor da empresa', 'Operador de dados', 'Espectador', 'Admins']