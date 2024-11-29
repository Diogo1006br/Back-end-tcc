from django.shortcuts import render
from rest_framework.views import APIView
from .models import Asset_DBTable
from rest_framework.response import Response
from Projects.models import Project_DBTable
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Utils.Mixins import Grupo_de_acesso_3Mixin,Grupo_de_acesso_1Mixin,Grupo_de_acesso_2Mixin
from rest_framework import status


# Create your views here.
class AssetNumbersView(APIView):
    
    def get(self, request,*args, **kwargs):
        """
        Retrieves the number of assets in system

        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :return: HTTP response with the number of assets in system.
        :rtype: rest_framework.response.Response

        :Request: GET api url/asset_numbers/<int:project>/
        
        """

        project = kwargs.get('project')
        return Response({'asset_numbers': Asset_DBTable.objects.filter(project=project).count()})

class AssetChangeStatus(APIView):
    
    def post(self, request, *args, **kwargs):
        """
        Changes the status of a asset

        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :param args: Additional arguments.
        :type args: tuple
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: HTTP response with the new status of the asset.
        :rtype: rest_framework.response.Response

        :Request: POST api url/change_asset_status/<int:id>/
        :Post data: {'status': 'new_status'}
        """
        mixin = Grupo_de_acesso_2Mixin()
        if not mixin.test_func(request):
            return Response(status=status.HTTP_403_FORBIDDEN)
        asset = Asset_DBTable.objects.get(id=kwargs.get('id'))
        projeto = asset.project
        if projeto.owner != request.user.companyId:
            return Response({'status': 'You do not have permission to change this asset status'}, status=401)
        else:
            asset.status = request.data.get('status')
            asset.save()
            return Response({'status': asset.status})
            
     
        