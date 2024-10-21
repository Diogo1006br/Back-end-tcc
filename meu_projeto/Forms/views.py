from django.shortcuts import render
from rest_framework.views import APIView
from .models import Form, FormResponse
from Registrations.models import Asset_DBTable 
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Utils.Mixins import Grupo_de_acesso_3Mixin,Grupo_de_acesso_1Mixin,Grupo_de_acesso_2Mixin
  # Import the mixin

# Create your views here.

class FormNumberView(APIView):
    @method_decorator(login_required)
    def get(self, request):
        """
        Retrieves the number of forms in system

        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :return: HTTP response with the number of forms in system.
        :rtype: rest_framework.response.Response

        :Request: GET api url/form_numbers/
        """
        mixin = Grupo_de_acesso_1Mixin()
        if not mixin.test_func(request):
            return mixin.handle_no_permission()
        return Response({'form_numbers': Form.objects.filter(company=request.user.companyId.id).count()})
    
class ChangeFormStatus(APIView):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        Changes the status of a form

        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :param args: Additional arguments.
        :type args: tuple
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: HTTP response with the new status of the form.
        :rtype: rest_framework.response.Response

        :Request: POST api url/change_form_status/<int:id>/
        :Post data: {'status': 'new_status'}
        
        """
        mixin = Grupo_de_acesso_2Mixin()
        if not mixin.test_func(request):
            return Response(status=status.HTTP_403_FORBIDDEN)
        form_id = kwargs.get('id')
        form = Form.objects.get(id=form_id)
        formcompany = form.company.id
        if formcompany != request.user.companyId.id:
            return Response({'message': 'Você não tem permissão para alterar o status deste formulário'})
        else:
            status = request.data.get('status')
            form.status = status
            form.save()
            return Response({'status': form.status})
    

class ResponsesByProject(APIView):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """
        Retrieves the number of responses by project

        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :param args: Additional arguments.
        :type args: tuple
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: HTTP response with the number of responses by project.
        :rtype: rest_framework.response.Response

        :Request: GET api url/responses_by_project/
        """
        mixin = Grupo_de_acesso_1Mixin()
        if not mixin.test_func(request):
            return Response(status=status.HTTP_403_FORBIDDEN)
        project = kwargs.get('project')
        assets = Asset_DBTable.objects.filter(project=project)
        form = kwargs.get('form')
        responses = FormResponse.objects.filter(form_id=form, object_id__in=assets.values_list('id', flat=True))

        DataReturn = []
        company = request.user.companyId.id
        for response in responses:

            if response.formID.company.id != company:
                return Response({'message': 'Você não tem permissão para acessar esses dados'})
            else:
                DataReturn.append({"response": response.response})

        return Response(DataReturn)
            
        


        
        