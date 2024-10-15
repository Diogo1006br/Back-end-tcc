from django.shortcuts import render
from .models import Project_DBTable
from .API.serializers import ProjectSerializer
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from Utils.Mixins import Grupo_de_acesso_1Mixin, Grupo_de_acesso_3Mixin, Grupo_de_acesso_2Mixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProjectNumberView(APIView):

    @method_decorator(login_required)
    def get(self, request):
        """
        Retrieves the number of projects in system

        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :return: HTTP response with the number of projects in system.
        :rtype: rest_framework.response.Response

        :Request: GET api url/project_numbers/
        """
        mixin = Grupo_de_acesso_1Mixin()
        if not mixin.test_func(request):
            return mixin.handle_no_permission()
        return Response({'project_numbers': Project_DBTable.objects.filter(members=request.user.id).count()})

class RecentProjectsView(APIView):
    @method_decorator(login_required)
    def get(self, request):
        """
        Retrieves the most recent projects in system

        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :return: HTTP response with the most recent projects in system.
        :rtype: rest_framework.response.Response

        :Request: GET api url/recent_projects/
        """
        mixin = Grupo_de_acesso_1Mixin()
        if not mixin.test_func(request):
            return mixin.handle_no_permission()
        max_last_projects = 5
        queryset = Project_DBTable.objects.filter(members=request.user).order_by('-uptaded_at')[:max_last_projects]

        serializer = ProjectSerializer(queryset, many=True)
        
        # Retorna os dados serializados
        return Response(serializer.data)

class ChangeProjectStatus(APIView):
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """
        Changes the status of a project

        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :param args: Additional arguments.
        :type args: tuple
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: HTTP response with the new status of the project.
        :rtype: rest_framework.response.Response

        :Request: POST api url/change_project_status/<int:id>/
        :Post data: {'status': 'new_status'}
        
        """
        mixin = Grupo_de_acesso_2Mixin()
        if not mixin.test_func(request):
            return Response(status=status.HTTP_403_FORBIDDEN)
        project_id = kwargs.get('id')
        project = Project_DBTable.objects.get(id=project_id)
        status = request.data.get('status')
        project.status = status
        project.save()
        return Response({'status': project.status})