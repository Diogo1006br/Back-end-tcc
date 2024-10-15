
from Forms.models import Form, FormResponse,DropboxAnswerList
from .serializers import FormSerializer,Form_ResponseSerializer,DropboxAnswerListSerializer,DropboxAnserListSerializerCompanyNameListing
from rest_framework import viewsets
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Registrations.models import Asset_DBTable, SubItem_DBTable, Asset_Sub_Element_DBTable
from django.contrib.auth.mixins import LoginRequiredMixin
from Utils.Mixins import Grupo_de_acesso_3Mixin,Grupo_de_acesso_1Mixin, Grupo_de_acesso_2Mixin


class FormsViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Form instances.

    :param queryset: The queryset that represents all forms.
    :type queryset: QuerySet
    :param serializer_class: The serializer class used to serialize and deserialize the Form instances.
    :type serializer_class: FormSerializer
    """
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    @method_decorator(login_required)
    def create(self, request, *args, **kwargs):
        """
        Create a new form.

        :param request: The request object.
        :type request: Request
        :param args: Additional arguments.
        :type args: list
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: The response object.
        :rtype: Response
        """
        mixin = Grupo_de_acesso_3Mixin()
        if not mixin.test_func(request):
            return mixin.handle_no_permission()
        company = request.user.companyId
        print(company)
        print(request.data)
        data = request.data
        data = {'name': data['name'],
                'form': data,
                'company': company.id}
        
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    @method_decorator(login_required)     
    def list (self, request, *args, **kwargs):
        """
        Get all forms.
        
        :param request: The request object.
        :type request: Request
        :param args: Additional arguments.
        :type args: list
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: The response object.
        :rtype: Response
        """
        mixin = Grupo_de_acesso_1Mixin()
        if not mixin.test_func(request):
            return mixin.handle_no_permission()
        company = request.user.companyId

        forms = Form.objects.filter(company=company.id)

        serializer = self.get_serializer(forms, many=True)

        return Response(serializer.data)



        return self.create(request, *args, **kwargs)
    @method_decorator(login_required)
    def retrieve(self, request, *args, **kwargs):
        mixin = Grupo_de_acesso_1Mixin()
        if not mixin.test_func(request):
            return mixin.handle_no_permission()
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        print(serializer.data)
        return super().retrieve(request, *args, **kwargs)
    @method_decorator(login_required)
    def update(self, request, *args, **kwargs):
        mixin = Grupo_de_acesso_3Mixin()
        if not mixin.test_func(request):
            return mixin.handle_no_permission()
        instance = self.get_object()
        data = request.data
        data = {'name': data['name'],
                'form': data,
                'company': instance.company.id}
        serializer = self.get_serializer(instance, data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)
        return Response(serializer.data)
    @method_decorator(login_required)
    def destroy(self, request, *args, **kwargs):
        mixin = Grupo_de_acesso_3Mixin()
        if not mixin.test_func(request):
            return mixin.handle_no_permission()
        id = self.get_object().id
        asset = Asset_DBTable.objects.filter(form=id).exists()
        subitem = SubItem_DBTable.objects.filter(form=id).exists()
        subelement = Asset_Sub_Element_DBTable.objects.filter(form=id).exists()
        if asset or subitem or subelement:
            return Response({'message': 'This form is being used by other tables'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return super().destroy(request, *args, **kwargs)


        
    

class Form_ResponseViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing FormResponse instances.

    :param queryset: The queryset that represents all form responses.
    :type queryset: QuerySet
    :param serializer_class: The serializer class used to serialize and deserialize the FormResponse instances.
    :type serializer_class: Form_ResponseSerializer
    """
    queryset = FormResponse.objects.all()
    serializer_class = Form_ResponseSerializer
    @method_decorator(login_required)
    def create (self, request, *args, **kwargs):
        """
        Create a new form response.

        :param request: The request object.
        :type request: Request
        :param args: Additional arguments.
        :type args: list
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: The response object.
        :rtype: Response
        """
        mixin = Grupo_de_acesso_2Mixin()
        if not mixin.test_func(request):
            return mixin.handle_no_permission(request)
        data = request.data
        Newdata = {'formID': data['formID'],
                'response': data['response'],
                'object_id': data['object_id'],
                'content_type':'',}
        
        if data['response_type'] == 'Asset':
            Newdata['content_type'] = ContentType.objects.get_for_model(Asset_DBTable)
        if data['response_type'] == 'Element':
            Newdata['content_type'] = ContentType.objects.get_for_model(SubItem_DBTable)
        if data['response_type'] == 'SubElement':
            Newdata['content_type'] = ContentType.objects.get_for_model(Asset_Sub_Element_DBTable)

        instance, created = self.get_queryset().update_or_create(
            object_id=Newdata['object_id'],
            content_type=Newdata['content_type'],
            defaults={'formID': Form.objects.get(id=Newdata['formID']), 'response': Newdata['response'], 'object_id': Newdata['object_id'], 'content_type': Newdata['content_type']}
        )

        if created:
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_200_OK

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status_code)
    @method_decorator(login_required)
    def list(self, request, *args, **kwargs):
        mixin = Grupo_de_acesso_1Mixin()
        if not mixin.test_func(request):
            return mixin.handle_no_permission()
        company = request.user.companyId
        params = request.query_params
        
        if 'formID' in params and 'Asset' in params and 'content_type' in params:
            if params['content_type'] == 'Asset':
                content_type = ContentType.objects.get_for_model(Asset_DBTable)

            elif params['content_type'] == 'Element':
                content_type = ContentType.objects.get_for_model(SubItem_DBTable)
            
            elif params['content_type'] == 'SubElement':
                content_type = ContentType.objects.get_for_model(Asset_Sub_Element_DBTable)
            else:
                return Response({'message': 'Invalid content_type'}, status=status.HTTP_400_BAD_REQUEST)

            responses = FormResponse.objects.get(formID=params['formID'], content_type=content_type, object_id=params['Asset'])
            
            # Verifica se há respostas antes de prosseguir
            if not responses:
                return Response({'message': 'No responses found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Verifica a permissão para a primeira resposta, assumindo que todas as respostas pertencem à mesma empresa
            if responses.formID.company != company:
                return Response('You do not have permission to view this form response', status=status.HTTP_403_FORBIDDEN)
            
            # Serializa e retorna todas as respostas se a permissão for válida
            serializer = Form_ResponseSerializer(responses)
            return Response(serializer.data)
        
        # Retorna uma resposta padrão se os parâmetros necessários não estiverem presentes
        return Response({'message': 'Missing required parameters'}, status=status.HTTP_400_BAD_REQUEST)

class DropBoxAnswerListViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing DropboxAnswerList instances.

    :param queryset: The queryset that represents all DropboxAnswerList instances.
    :type queryset: QuerySet
    :param serializer_class: The serializer class used to serialize and deserialize the DropboxAnswerList instances.
    :type serializer_class: DropboxAnswerListSerializer
    """
    queryset = DropboxAnswerList.objects.all()
    serializer_class = DropboxAnswerListSerializer
    @method_decorator(login_required)
    def create(self, request, *args, **kwargs):
        """
        Create a new DropboxAnswerList.

        :param request: The request object.
        :type request: Request
        :param args: Additional arguments.
        :type args: list
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: The response object.
        :rtype: Response
        """
        mixin = Grupo_de_acesso_3Mixin()
        if not mixin.test_func(request):
            return mixin.handle_no_permission()
        data = request.data
        newData = { 'name': data['name'],
                    'list': data['list'],
                    'company': request.user.companyId.id
                    }
                   
        serializer = self.get_serializer(data=newData)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    @method_decorator(login_required)
    def update(self, request, *args, **kwargs):
        """
        Update a DropboxAnswerList. 

        :param request: The request object.
        :type request: Request
        :param args: Additional arguments.
        :type args: list
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: The response object.
        :rtype: Response
        """
        mixin = Grupo_de_acesso_3Mixin()
        if not mixin.test_func(request):
            return mixin.handle_no_permission()
        instance = self.get_object()
        data = request.data
        newData = { 'name': data['name'],
                    'list': data['list'],
                    'company': request.user.companyId.id
                    }
        serializer = self.get_serializer(instance, data=newData)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @method_decorator(login_required)
    def list(self, request, *args, **kwargs):
        """
        List all DropboxAnswerLists.

        :param request: The request object.
        :type request: Request
        :param args: Additional arguments.
        :type args: list
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: The response object.
        :rtype: Response
        """
        mixin = Grupo_de_acesso_1Mixin()
        if not mixin.test_func(request):
            return mixin.handle_no_permission()
        company = request.user.companyId
        lists = DropboxAnswerList.objects.filter(company=company.id)

        serializer = DropboxAnserListSerializerCompanyNameListing(lists, many=True)
         
        return Response(serializer.data)
    @method_decorator(login_required)
    def destroy(self, request, *args, **kwargs):
        """
        Delete a DropboxAnswerList.
        """
        mixin = Grupo_de_acesso_3Mixin()
        if not mixin.test_func(request):
            return mixin.handle_no_permission()
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Deleted successfully'}, status=status.HTTP_200_OK)