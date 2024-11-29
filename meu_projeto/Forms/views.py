from django.shortcuts import render
from rest_framework.views import APIView
from .models import Form, FormResponse
from Registrations.models import Asset_DBTable
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework import status
from django.utils.decorators import method_decorator
from Utils.Mixins import Grupo_de_acesso_3Mixin, Grupo_de_acesso_1Mixin, Grupo_de_acesso_2Mixin


class FormNumberView(APIView):
    
    def get(self, request):
        """
        Retrieves the number of forms in the system.

        :param request: HTTP request object.
        :return: HTTP response with the number of forms in the system.
        """
        form_count = Form.objects.filter(company=1).count()
        return Response({'form_numbers': form_count})


class ChangeFormStatus(APIView):
    
    def post(self, request, *args, **kwargs):
        """
        Changes the status of a form.

        :param request: HTTP request object.
        :param kwargs: URL parameters, including form ID.
        :return: HTTP response with the updated status of the form.
        """
        form_id = kwargs.get('id')
        form = Form.objects.get(id=form_id)
        form.status = request.data.get('status')
        form.save()
        return Response({'status': form.status})


class ResponsesByProject(APIView):
    
    def get(self, request, *args, **kwargs):
        """
        Retrieves the responses associated with a project.

        :param request: HTTP request object.
        :param kwargs: URL parameters, including project and form IDs.
        :return: HTTP response with the list of responses.
        """
        mixin = Grupo_de_acesso_1Mixin()
        if not mixin.test_func(request):
            return Response(status=status.HTTP_403_FORBIDDEN)

        project = kwargs.get('project')
        form_id = kwargs.get('form')
        assets = Asset_DBTable.objects.filter(project=project)
        responses = FormResponse.objects.filter(formID=form_id, object_id__in=assets.values_list('id', flat=True))

        if not responses:
            return Response({'message': 'Nenhuma resposta encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        company = request.user.companyId.id
        data_return = []
        for response in responses:
            if response.formID.company.id != company:
                return Response({'message': 'Você não tem permissão para acessar esses dados.'},
                                status=status.HTTP_403_FORBIDDEN)
            data_return.append({"response": response.response})

        return Response(data_return)


class DuplicateForm(APIView):
    
    def post(self, request, *args, **kwargs):
        """
        Duplicates a form.

        :param request: HTTP request object.
        :param kwargs: URL parameters, including form ID.
        :return: HTTP response with the ID of the duplicated form.
        """
        mixin = Grupo_de_acesso_2Mixin()
        if not mixin.test_func(request):
            return Response(status=status.HTTP_403_FORBIDDEN)

        form_id = kwargs.get('id')
        form = Form.objects.get(id=form_id)
        if form.company.id != request.user.companyId.id:
            return Response({'message': 'Você não tem permissão para duplicar este formulário.'},
                            status=status.HTTP_403_FORBIDDEN)

        new_form = Form.objects.create(
            name=f'{form.name} (Cópia)',
            form=form.form,
            company=form.company,
            status=form.status,
        )
        return Response({'form': new_form.id}, status=status.HTTP_201_CREATED)
