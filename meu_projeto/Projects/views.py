from django.shortcuts import get_object_or_404
from .models import Project_DBTable
from .API.serializers import ProjectSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from Utils.Mixins import Grupo_de_acesso_1Mixin, Grupo_de_acesso_3Mixin, Grupo_de_acesso_2Mixin

class ProjectNumberView(Grupo_de_acesso_1Mixin, APIView):
    def get(self, request):
        if not self.test_func():
            return self.handle_no_permission()
        
        project_count = Project_DBTable.objects.filter(members=request.user.id).count()
        return Response({'project_numbers': project_count})

class RecentProjectsView(Grupo_de_acesso_1Mixin, APIView):
    def get(self, request):
        if not self.test_func():
            return self.handle_no_permission()
        
        max_last_projects = 5
        queryset = Project_DBTable.objects.filter(members=request.user).order_by('-updated_at')[:max_last_projects]
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

class ChangeProjectStatus(Grupo_de_acesso_2Mixin, APIView):
    def post(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()
        
        project_id = kwargs.get('id')
        if project_id is None:
            return Response({"error": "Project ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        project = get_object_or_404(Project_DBTable, id=project_id)
        new_status = request.data.get('status')
        
        if not new_status:
            return Response({'error': 'Status not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        project.status = new_status
        project.save()
        return Response({'status': project.status}, status=status.HTTP_200_OK)
