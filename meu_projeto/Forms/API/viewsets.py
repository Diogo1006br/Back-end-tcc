from Forms.models import Form, FormResponse, DropboxAnswerList
from .serializers import FormSerializer, Form_ResponseSerializer, DropboxAnswerListSerializer, DropboxAnserListSerializerCompanyNameListing
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Registrations.models import Asset_DBTable, SubItem_DBTable, Asset_Sub_Element_DBTable
from Utils.Mixins import Grupo_de_acesso_3Mixin, Grupo_de_acesso_1Mixin, Grupo_de_acesso_2Mixin
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import requests


class FormsViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer

    
    def create(self, request, *args, **kwargs):
        company = 1
        data = {'name': request.data['name'], 'form': request.data, 'company': company}
        
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    def list(self, request, *args, **kwargs):
        forms = Form.objects.filter(company=1)
        serializer = self.get_serializer(forms, many=True)
        
        return Response(serializer.data)

    
    def retrieve(self, request, *args, **kwargs):

        
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = {'name': request.data['name'], 'form': request.data, 'company': instance.company.id}
        
        serializer = self.get_serializer(instance, data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        return Response(serializer.data)

    
    def destroy(self, request, *args, **kwargs):
        id = self.get_object().id
        asset = Asset_DBTable.objects.filter(form=id).exists()
        subitem = SubItem_DBTable.objects.filter(form=id).exists()
        subelement = Asset_Sub_Element_DBTable.objects.filter(form=id).exists()
        
        if asset or subitem or subelement:
            return Response({'message': 'This form is being used by other tables'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return super().destroy(request, *args, **kwargs)


class Form_ResponseViewSet(viewsets.ModelViewSet):
    queryset = FormResponse.objects.all()
    serializer_class = Form_ResponseSerializer

    
    def create(self, request, *args, **kwargs):
        data = request.data

        # Iterar sobre os campos da resposta e tratar os valores adequadamente
        for key, value in data['response'].items():
            if isinstance(value, str) and 'https' in value:  # Verifica se é uma string e contém 'https'
                image_url = value
                response = requests.get(image_url)
                if response.status_code == 200:
                    if settings.DEBUG:
                        file_path = f'local_images/{key}.jpg'
                        with open(file_path, 'wb') as f:
                            f.write(response.content)
                        data['response'][key] = file_path
                    else:
                        file_name = f'{key}.jpg'
                        file_content = ContentFile(response.content)
                        file_path = default_storage.save(file_name, file_content)
                        data['response'][key] = default_storage.url(file_path)
            elif isinstance(value, bool):
                # Tratamento específico para valores booleanos (se necessário)
                print(f"Campo {key} é um valor booleano: {value}")
            else:
                # Ignorar outros tipos de valores, ou adicionar tratamento adicional
                print(f"Campo {key} possui um tipo ignorado: {value}")

        # Montar os dados para criar ou atualizar a resposta
        Newdata = {
            'formID': data['formID'],
            'response': data['response'],
            'object_id': data['object_id'],
            'content_type': ''
        }
        
        # Determinar o tipo de conteúdo com base no tipo de resposta
        if data['response_type'] == 'Asset':
            Newdata['content_type'] = ContentType.objects.get_for_model(Asset_DBTable)
        elif data['response_type'] == 'Element':
            Newdata['content_type'] = ContentType.objects.get_for_model(SubItem_DBTable)
        elif data['response_type'] == 'SubElement':
            Newdata['content_type'] = ContentType.objects.get_for_model(Asset_Sub_Element_DBTable)

        # Criar ou atualizar a instância no banco de dados
        instance, created = self.get_queryset().update_or_create(
            object_id=Newdata['object_id'],
            content_type=Newdata['content_type'],
            defaults={'formID': Form.objects.get(id=Newdata['formID']), 'response': Newdata['response']}
        )

        # Determinar o código de status apropriado
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status_code)


    
    def list(self, request, *args, **kwargs):

        
        company = 1
        params = request.query_params
        
        if 'formID' in params and 'Asset' in params and 'content_type' in params:
            content_type = ContentType.objects.get_for_model({
                'Asset': Asset_DBTable,
                'Element': SubItem_DBTable,
                'SubElement': Asset_Sub_Element_DBTable
            }[params['content_type']])
            
            responses = FormResponse.objects.filter(
                formID=params['formID'],
                content_type=content_type,
                object_id=params['Asset']
            )
            
            if not responses.exists():
                return Response({'message': 'No responses found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = Form_ResponseSerializer(responses, many=True)
            return Response(serializer.data)
        
        return Response({'message': 'Missing required parameters'}, status=status.HTTP_400_BAD_REQUEST)


class DropBoxAnswerListViewSet(viewsets.ModelViewSet):
    queryset = DropboxAnswerList.objects.all()
    serializer_class = DropboxAnswerListSerializer

    
    def create(self, request, *args, **kwargs):
        newData = {
            'name': request.data['name'],
            'list': request.data['list'],
            'company': request.user.companyId.id
        }
        
        serializer = self.get_serializer(data=newData)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        newData = {
            'name': request.data['name'],
            'list': request.data['list'],
            'company': request.user.companyId.id
        }
        
        serializer = self.get_serializer(instance, data=newData)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def list(self, request, *args, **kwargs):

        
        company = request.user.companyId
        lists = DropboxAnswerList.objects.filter(company=company.id)
        serializer = DropboxAnserListSerializerCompanyNameListing(lists, many=True)
        
        return Response(serializer.data)

    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Deleted successfully'}, status=status.HTTP_200_OK)
