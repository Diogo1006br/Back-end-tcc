from django.shortcuts import render
from rest_framework.views import APIView
from .models import Asset_DBTable
from rest_framework.response import Response
from Projects.models import Project_DBTable

class AssetNumbersView(APIView):
    def get(self, request, *args, **kwargs):
        project = kwargs.get('project')
        owner = Project_DBTable.objects.get(id=project).owner
        
        if owner != request.user.companyId:
            return Response({'asset_numbers': 'You do not have permission to view this project assets'}, status=401)
        
        return Response({'asset_numbers': Asset_DBTable.objects.filter(project=project).count()})

class AssetChangeStatus(APIView):
    def post(self, request, *args, **kwargs):
        asset = Asset_DBTable.objects.get(id=kwargs.get('id'))
        projeto = asset.project
        
        if projeto.owner != request.user.companyId:
            return Response({'status': 'You do not have permission to change this asset status'}, status=401)
        
        asset.status = request.data.get('status')
        asset.save()
        
        return Response({'status': asset.status})
