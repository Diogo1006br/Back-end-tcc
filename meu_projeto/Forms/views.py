from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Form, FormResponse
from Registrations.models import Asset_DBTable
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Utils.Mixins import Grupo_de_acesso_3Mixin, Grupo_de_acesso_1Mixin, Grupo_de_acesso_2Mixin

class FormNumberView(Grupo_de_acesso_1Mixin, APIView):
    renderer_classes = [JSONRenderer]  # Explicitly set JSON renderer

    @method_decorator(login_required)
    def get(self, request):
        """
        Retrieves the number of forms in the system.
        """
        if not self.test_func():
            return self.handle_no_permission()
        
        form_count = Form.objects.filter(company=request.user.companyId.id).count()
        return Response({'form_numbers': form_count}, status=status.HTTP_200_OK)

class ChangeFormStatus(Grupo_de_acesso_2Mixin, APIView):
    renderer_classes = [JSONRenderer]  # Explicitly set JSON renderer

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        Changes the status of a form.
        """
        if not self.test_func():
            return self.handle_no_permission()
        
        form_id = kwargs.get('id')
        form = Form.objects.get(id=form_id)
        
        if form.company.id != request.user.companyId.id:
            return Response({'message': 'Você não tem permissão para alterar o status deste formulário'}, status=status.HTTP_403_FORBIDDEN)
        
        new_status = request.data.get('status')
        form.status = new_status
        form.save()
        return Response({'status': form.status}, status=status.HTTP_200_OK)

class ResponsesByProject(Grupo_de_acesso_1Mixin, APIView):
    renderer_classes = [JSONRenderer]  # Explicitly set JSON renderer

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        Retrieves the number of responses by project.
        """
        if not self.test_func():
            return self.handle_no_permission()
        
        project_id = kwargs.get('project')
        form_id = kwargs.get('form')
        
        assets = Asset_DBTable.objects.filter(project=project_id)
        responses = FormResponse.objects.filter(form_id=form_id, object_id__in=assets.values_list('id', flat=True))
        
        company_id = request.user.companyId.id
        response_data = []

        for response in responses:
            if response.formID.company.id != company_id:
                return Response({'message': 'Você não tem permissão para acessar esses dados'}, status=status.HTTP_403_FORBIDDEN)
            response_data.append({"response": response.response})

        return Response(response_data, status=status.HTTP_200_OK)
