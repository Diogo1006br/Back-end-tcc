from Forms.models import Form, FormResponse, DropboxAnswerList
from .serializers import FormSerializer, Form_ResponseSerializer, DropboxAnswerListSerializer, DropboxAnserListSerializerCompanyNameListing
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Registrations.models import Asset_DBTable, SubItem_DBTable, Asset_Sub_Element_DBTable
from Utils.Mixins import Grupo_de_acesso_3Mixin, Grupo_de_acesso_1Mixin, Grupo_de_acesso_2Mixin

class FormsViewSet(Grupo_de_acesso_3Mixin, viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer

    @method_decorator(login_required)
    def create(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()

        company = request.user.companyId
        data = {
            'name': request.data['name'],
            'form': request.data,
            'company': company.id
        }
        
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(login_required)
    def list(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()

        company = request.user.companyId
        forms = Form.objects.filter(company=company.id)
        serializer = self.get_serializer(forms, many=True)
        return Response(serializer.data)

    @method_decorator(login_required)
    def retrieve(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @method_decorator(login_required)
    def update(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()

        instance = self.get_object()
        data = {
            'name': request.data['name'],
            'form': request.data,
            'company': instance.company.id
        }
        serializer = self.get_serializer(instance, data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response(serializer.data)

    @method_decorator(login_required)
    def destroy(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()

        form_id = self.get_object().id
        if Asset_DBTable.objects.filter(form=form_id).exists() or \
           SubItem_DBTable.objects.filter(form=form_id).exists() or \
           Asset_Sub_Element_DBTable.objects.filter(form=form_id).exists():
            return Response({'message': 'This form is being used by other tables'}, status=status.HTTP_400_BAD_REQUEST)

        return super().destroy(request, *args, **kwargs)

class Form_ResponseViewSet(Grupo_de_acesso_2Mixin, viewsets.ModelViewSet):
    queryset = FormResponse.objects.all()
    serializer_class = Form_ResponseSerializer

    @method_decorator(login_required)
    def create(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()

        data = request.data
        Newdata = {
            'formID': data['formID'],
            'response': data['response'],
            'object_id': data['object_id'],
            'content_type': ContentType.objects.get_for_model({
                'Asset': Asset_DBTable,
                'Element': SubItem_DBTable,
                'SubElement': Asset_Sub_Element_DBTable
            }.get(data['response_type']))
        }
        
        instance, created = self.get_queryset().update_or_create(
            object_id=Newdata['object_id'],
            content_type=Newdata['content_type'],
            defaults={'formID': Form.objects.get(id=Newdata['formID']), 'response': Newdata['response']}
        )

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @method_decorator(login_required)
    def list(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()

        company = request.user.companyId
        params = request.query_params
        if 'formID' in params and 'Asset' in params and 'content_type' in params:
            content_type = ContentType.objects.get_for_model({
                'Asset': Asset_DBTable,
                'Element': SubItem_DBTable,
                'SubElement': Asset_Sub_Element_DBTable
            }.get(params['content_type']))

            responses = FormResponse.objects.filter(formID=params['formID'], content_type=content_type, object_id=params['Asset'])
            if not responses.exists():
                return Response({'message': 'No responses found'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = Form_ResponseSerializer(responses, many=True)
            return Response(serializer.data)

        return Response({'message': 'Missing required parameters'}, status=status.HTTP_400_BAD_REQUEST)

class DropBoxAnswerListViewSet(Grupo_de_acesso_3Mixin, viewsets.ModelViewSet):
    queryset = DropboxAnswerList.objects.all()
    serializer_class = DropboxAnswerListSerializer

    @method_decorator(login_required)
    def create(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()

        data = {
            'name': request.data['name'],
            'list': request.data['list'],
            'company': request.user.companyId.id
        }
        
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @method_decorator(login_required)
    def update(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()

        instance = self.get_object()
        data = {
            'name': request.data['name'],
            'list': request.data['list'],
            'company': request.user.companyId.id
        }
        
        serializer = self.get_serializer(instance, data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(login_required)
    def list(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()

        company = request.user.companyId
        lists = DropboxAnswerList.objects.filter(company=company.id)
        serializer = DropboxAnserListSerializerCompanyNameListing(lists, many=True)
        return Response(serializer.data)

    @method_decorator(login_required)
    def destroy(self, request, *args, **kwargs):
        if not self.test_func():
            return self.handle_no_permission()

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Deleted successfully'}, status=status.HTTP_200_OK)
