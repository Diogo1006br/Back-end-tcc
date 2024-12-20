from django.shortcuts import get_object_or_404
from .models import Project_DBTable
from .API.serializers import ProjectSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from Utils.Mixins import Grupo_de_acesso_1Mixin, Grupo_de_acesso_2Mixin
from rest_framework.renderers import JSONRenderer

class ProjectNumberView(Grupo_de_acesso_1Mixin, APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        project_count = Project_DBTable.objects.filter(members=1).count()
        return Response({'project_numbers': project_count})


class RecentProjectsView(Grupo_de_acesso_1Mixin, APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        recent_projects = Project_DBTable.objects.filter(members=1).order_by('-created_at')[:5]
        project_data = [{'id': project.id, 'name': project.projectName} for project in recent_projects]
        return Response({'recent_projects': project_data})


class ChangeProjectStatus(Grupo_de_acesso_2Mixin, APIView):
    def patch(self, request, *args, **kwargs):
        project_id = kwargs.get('id')
        if project_id is None:
            return Response({"error": "Project ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            project = Project_DBTable.objects.get(id=project_id)
        except Project_DBTable.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        if not new_status:
            return Response({'error': 'Status not provided'}, status=status.HTTP_400_BAD_REQUEST)

        allowed_statuses = ['Pending', 'In Progress', 'Completed']
        if new_status not in allowed_statuses:
            return Response({'error': 'Invalid status provided'}, status=status.HTTP_400_BAD_REQUEST)

        project.status = new_status
        project.save()

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)
