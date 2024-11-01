from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from .models import Form, FormResponse
from Registrations.models import Asset_DBTable
from Utils.Mixins import Grupo_de_acesso_1Mixin, Grupo_de_acesso_2Mixin

class FormNumberView(Grupo_de_acesso_1Mixin, APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]  # Garante que o usuário esteja autenticado

    def get(self, request):
        if not self.test_func():
            return self.handle_no_permission()
        
        form_count = Form.objects.filter(company=request.user.companyId.id).count()
        return Response({'form_numbers': form_count}, status=status.HTTP_200_OK)

class ChangeFormStatus(Grupo_de_acesso_2Mixin, APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()
        
        form_id = kwargs.get('id')
        try:
            form = Form.objects.get(id=form_id, company=request.user.companyId)
        except Form.DoesNotExist:
            return Response({'message': 'Formulário não encontrado ou permissão negada'}, status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get('status')
        form.status = new_status
        form.save()
        return Response({'status': form.status}, status=status.HTTP_200_OK)

class ResponsesByProject(Grupo_de_acesso_1Mixin, APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()
        
        project_id = kwargs.get('project')
        form_id = kwargs.get('form')

        assets = Asset_DBTable.objects.filter(project=project_id)
        responses = FormResponse.objects.filter(form_id=form_id, object_id__in=assets.values_list('id', flat=True))
        
        company_id = request.user.companyId.id
        response_data = [
            {"response": response.response}
            for response in responses if response.form_id.company.id == company_id
        ]

        if not response_data:
            return Response({'message': 'Você não tem permissão para acessar esses dados'}, status=status.HTTP_403_FORBIDDEN)

        return Response(response_data, status=status.HTTP_200_OK)
