from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q
from .serializers import AssetDBTableSerializer,SubItemDBTableSerializer,AssetSubElementSerializer,imagesSerializer,ActionDBTableSerializer,CommentSerializer,AssetDBTableSerializerwithformname
from Registrations.models import Asset_DBTable,SubItem_DBTable,Asset_Sub_Element_DBTable,images,Action_DBTable,Comment_DBTable
from Forms.models import Form
from Projects.models import Project_DBTable
from django.contrib.contenttypes.models import ContentType
from Projects.models import Project_DBTable
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from Accounts.models import CustomUser_DBTable
from Utils.Mixins import Grupo_de_acesso_3Mixin,Grupo_de_acesso_1Mixin, Grupo_de_acesso_2Mixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class CommentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing comment instances.

    :param queryset: The queryset that represents all comment instances.
    :type queryset: QuerySet
    :param serializer_class: The serializer class used to serialize and deserialize the comment instances.
    :type serializer_class: CommentSerializer
    """
    queryset = Comment_DBTable.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new comment instance.

        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :param args: Additional arguments.
        :type args: list
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: HTTP response with the comment instance.
        :rtype: rest_framework.response.Response

        :to use in front call the api with that example
        :use api.post('/api/comment/', {comment: 'Comentário 1', content_type: 'Asset', object_id: 1})
        :The data that return is the comment that have the comment 'Comentário 1'

        """

        comment = request.data.get('comment')
        content_type = request.data.get('content_type')
        if content_type == 'Asset':
            content_type = ContentType.objects.get_for_model(Asset_DBTable)
        elif content_type == 'Element':
            content_type = ContentType.objects.get_for_model(SubItem_DBTable)
        elif content_type == 'SubElement':
            content_type = ContentType.objects.get_for_model(Asset_Sub_Element_DBTable)
        else:
            return Response({'status': 'Error creating comment', 'error': f'{content_type} is a invalid content type'}, status=status.HTTP_400_BAD_REQUEST)

        object_id = request.data.get('object_id')
        user = request.user
        questionKey = request.data.get('questionKey')
        obj , create = Comment_DBTable.objects.update_or_create(comment=comment, content_type=content_type, object_id=object_id, user=user, questionKey=questionKey)
        return Response({'status': 'Comment created successfully'}, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        """
        List all comment instances.

        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :param args: Additional arguments.
        :type args: list
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: HTTP response with the comment instances.
        :rtype: rest_framework.response.Response

        :to use in front call the api with that example
        :use api.get('/api/comment/', {params: {questionKey: 'questionkey'}})
        :The data that return is the comment that have the questionKey 'questionkey'

        """

        params = request.query_params
        if 'content_type' and 'object_id' in params:
            contentType = params.get('content_type')
            object_id = params.get('object_id')

            if contentType == 'Asset':
                contentType = ContentType.objects.get_for_model(Asset_DBTable)
            if contentType == 'Element':
                contentType = ContentType.objects.get_for_model(SubItem_DBTable)
            if contentType == 'SubElement':
                contentType = ContentType.objects.get_for_model(Asset_Sub_Element_DBTable)
            queryset = self.get_queryset().filter(content_type=contentType, object_id=object_id)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'Object_id ou content_type nao informado'}, status=status.HTTP_400_BAD_REQUEST)
class ActionPerItemViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing action instances.

    :param queryset: The queryset that represents all action instances.
    :type queryset: QuerySet
    :param serializer_class: The serializer class used to serialize and deserialize the action instances.
    :type serializer_class: ActionSerializer
    """
    def send_html_email(self, to_list, subject, template_name, context, from_email=None):
        print('CHEGUEI NA FUNÇÃO....')
        html_content = render_to_string(template_name, context)  # renderiza o template HTML com o contexto
        email = EmailMessage(subject, html_content, from_email, to_list)
        email.content_subtype = "html"  # Define o conteúdo do e-mail como HTML
        email.send()
        print('EMAIL ENVIADO....')
    queryset = Action_DBTable.objects.all()
    serializer_class = ActionDBTableSerializer

    
    def list(self, request, *args, **kwargs):
        """
        List all action instances.

        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :param args: Additional arguments.
        :type args: list
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: HTTP response with the action instances.
        :rtype: rest_framework.response.Response

        :to use in front call the api with that example
        :use api.get('/api/action/1/')
        :The data that return is the action that have the title 'Ação 1'

        """
        

        request_user = request.user
        request_user = self.request.user
        object_id = request.query_params.get('object_id')
        content_type_param = request.query_params.get('content_type')

        if content_type_param == 'Asset':
            content_type = ContentType.objects.get_for_model(Asset_DBTable)
        elif content_type_param == 'Element':
            content_type = ContentType.objects.get_for_model(SubItem_DBTable)
        elif content_type_param == 'SubElement':
            content_type = ContentType.objects.get_for_model(Asset_Sub_Element_DBTable)
        queryset = super().get_queryset().filter(
            object_id=object_id, content_type=content_type
        )
        serializer = self.get_serializer(queryset, many=True)        
        return Response(serializer.data)

class ActionViewSet(viewsets.ModelViewSet):
    
    """
    A viewset for viewing and editing action instances.

    :param queryset: The queryset that represents all action instances.
    :type queryset: QuerySet
    :param serializer_class: The serializer class used to serialize and deserialize the action instances.
    :type serializer_class: ActionSerializer
    """
    def send_html_email(self, to_list, subject, template_name, context, from_email=None):
        print('CHEGUEI NA FUNÇÃO....')
        html_content = render_to_string(template_name, context)  # renderiza o template HTML com o contexto
        email = EmailMessage(subject, html_content, from_email, to_list)
        email.content_subtype = "html"  # Define o conteúdo do e-mail como HTML
        email.send()
        print('EMAIL ENVIADO....')
    queryset = Action_DBTable.objects.all()
    serializer_class = ActionDBTableSerializer

    
    def list(self, request, *args, **kwargs):
        """
        List all action instances.

        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :param args: Additional arguments.
        :type args: list
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: HTTP response with the action instances.
        :rtype: rest_framework.response.Response

        :to use in front call the api with that example
        :use api.get('/api/action/')
        :The data that return is the action that have the title 'Ação 1'

        """
        

        request_user = request.user
        request_user = self.request.user
        queryset = super().get_queryset().filter(
            Q(responsible=request_user) | Q(user_hasCreated=request_user)
        )
        serializer = self.get_serializer(queryset, many=True)        
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        Create a new action instance.

        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :param args: Additional arguments.
        :type args: list
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: HTTP response with the action instance.
        :rtype: rest_framework.response.Response

        :to use in front call the api with that example
        :use api.post('/api/action/', {title: 'Ação 1', content_type: 'Asset', object_id: 1, priority: 'Baixa', deadline: '2021-12-31', responsible: 1})
        :The data that return is the action that have the title 'Ação 1'
        """

        title = request.data.get('title')
        content_type = request.data.get('content_type')
        if content_type == 'Asset':
            content_type = ContentType.objects.get_for_model(Asset_DBTable)
        elif content_type == 'Element':
            content_type = ContentType.objects.get_for_model(SubItem_DBTable)
        elif content_type == 'SubElement':
            content_type = ContentType.objects.get_for_model(Asset_Sub_Element_DBTable)
        else:
            return Response({'status': 'Error creating action', 'error': f'{content_type} is a invalid content type'}, status=status.HTTP_400_BAD_REQUEST)

        object_id = request.data.get('object_id')
        priority = request.data.get('priority')
        deadline = request.data.get('deadline')
        user_email = request.data.get('responsible_email')

        if request.data.get('questionKey'):
            questionKey = request.data.get('questionKey')
        else:
            questionKey = ''

        if not user_email:
            return Response({'status': 'Error creating action', 'error': 'User email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            responsible = CustomUser_DBTable.objects.get(email=user_email)
        except CustomUser_DBTable.DoesNotExist:
            return Response({'status': 'Error creating action', 'error': f'User {user_email} not found'}, status=status.HTTP_400_BAD_REQUEST)

        place = request.data.get('place')
        description = request.data.get('description')
        user_hasCreated = request.user
        action_status = request.data.get('status')

        try:
            if not user_email:
                raise ValueError("user_email is required")
            if not request.user.email:
                raise ValueError("request.user.email is required")
            if not title:
                raise ValueError("title is required")

            context = {
                'email': user_email,
                'Inviter': request.user.email,
                'title': title,
            }
            self.send_html_email([user_email], 'Invite Aria-IO', 'Action.html', context, settings.EMAIL_HOST_USER)

            action = Action_DBTable.objects.create(
                title=title,
                content_type=content_type,
                object_id=object_id,
                priority=priority,
                deadline=deadline,
                responsible=responsible,
                place=place,
                description=description,
                user_hasCreated=user_hasCreated,
                status=action_status,
                questionKey=questionKey
            )
            action.save()
            return Response({'status': 'Action created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': 'Error creating action', 'error': str(e), 'responsible_email': user_email}, status=status.HTTP_400_BAD_REQUEST)
class AssetDBTableViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Asset_DBTable instances.
    This viewset dynamically returns a queryset based on the 'projeto' query parameter
    and uses different serializers for GET and POST requests.
    """

    """
    Optionally restricts the returned assets to a given project,
    by filtering against a `projeto` query parameter in the URL.
    """
    queryset = Asset_DBTable.objects.all()
    serializer_class = AssetDBTableSerializer
    
    def list(self, request, *args, **kwargs):
        """
        List all Asset_DBTable instances.

        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :param args: Additional arguments.
        :type args: list
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: HTTP response with the Asset_DBTable instances.
        :rtype: rest_framework.response.Response

        :to use in front call the api with that example
        :use api.get('/api/asset/', {params: {project: 1}})
        :The data that return is the asset that is in the project 1
        :representated by that json
        :{
        :    "id": 1,
        :    "assetName": "Ativo 1",
        :    "form": 1,
        :    "project": 1,
        :    "status": "Ativo"
        :}

        """
        
        # Usando request.query_params em vez de request.data
        params = request.query_params

        if 'project' in params:
            projeto = params.get('project')
                
            queryset = self.get_queryset().filter(project=projeto)
            for query in queryset:
                if query.is_ocult == True:
                    if request.user not in query.show_to.all():
                        queryset = queryset.exclude(pk=query.pk)
            serializer = AssetDBTableSerializerwithformname(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user = request.user
            projects = Project_DBTable.objects.filter(members=user)
            queryset = self.get_queryset().filter(project__in=projects)
            serializer = AssetDBTableSerializerwithformname(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        
        
    
    def create(self, request, *args, **kwargs):
        """
        Create a new Asset_DBTable instance.

        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :param args: Additional arguments.
        :type args: list
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: HTTP response with the Asset_DBTable instance.
        :rtype: rest_framework.response.Response

        :to use in front call the api with that example
        :use api.post('/api/asset/', {assetName: 'Ativo 1', form: 1, project: 1, status: 'Ativo'})
        :The data that return is the asset that is in the project 1
        :representated by that json
        :{
        :    "id": 1,
        :    "assetName": "Ativo 1",
        :    "form": 1,
        :    "project": 1,
        :    "status": "Ativo"
        :}
        """
        data = request.data
        is_ocult = data.get('is_ocult') == 'true'

        new_data = {
            'assetName': data.get('assetName'),
            'form': Form.objects.get(pk=data.get('form')),
            'project': Project_DBTable.objects.get(pk=data.get('project')),
            'is_ocult': is_ocult,
        }
        try:
            asset = Asset_DBTable.objects.create(**new_data)
            asset.save()
            
            show_to_emails = data.getlist('show_to[]')
            print(show_to_emails)
            if show_to_emails:
                asset.show_to.set(CustomUser_DBTable.objects.filter(email__in=show_to_emails))
            
            return Response({'id': asset.id, 'status': 'Asset created successfully', 'show_to_data':show_to_emails}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'status': 'Asset not created', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a Asset_DBTable instance.

        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :param args: Additional arguments.
        :type args: list
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: HTTP response with the Asset_DBTable instance.
        :rtype: rest_framework.response.Response

        :to use in front call the api with that example
        :use api.delete('/api/asset/1/')
        :The data that return is the asset that is in the project 1
        :representated by that json
        :{
        :    "id": 1,
        :    "assetName": "Ativo 1",
        :    "form": 1,
        :    "project": 1,
        :    "status": "Ativo"
        :}
        """
        instance = self.get_object()
        subItems = SubItem_DBTable.objects.filter(ativo=instance.id)
        try:
            for item in subItems:
                item.delete()
            instance.delete()  # Deletar a instância de Asset_DBTable
            return Response({'status': 'Asset deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'status': 'Error deleting asset', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SubItemDBTableViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Element_Ativo_DBTable instances.

    :param queryset: The queryset that represents all Element_Ativo_DBTable instances.
    :type queryset: QuerySet
    :param serializer_class: The serializer class used to serialize and deserialize the Element_Ativo_DBTable instances.
    :type serializer_class: ElementAtivoDBTableSerializer
    
    """
    queryset = SubItem_DBTable.objects.all()
    serializer_class = SubItemDBTableSerializer
    
    def list(self, request, *args, **kwargs):
        """
        List all Asset_Element_DBTable instances.

        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :param args: Additional arguments.
        :type args: list
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: HTTP response with the Asset_Element_DBTable instances.
        :rtype: rest_framework.response.Response

        :to use in front call the api with that example
        :use api.get('/api/element/')
        :The data that return is the element that is in the asset 1
        :representated by that json
        :{
        :    "id": 1,
        :    "elementName": "Elemento 1",
        :    "ativo": 1,
        :    "form": 1
        :}
        """
        user = request.user
        projetos = Project_DBTable.objects.filter(members=user)
        assets =  Asset_DBTable.objects.filter(project__in=projetos)
        queryset = self.get_queryset().filter(asset__in=assets)
        newqueryset = []
        for query in queryset:
            if query.is_ocult == False:
                newqueryset.append(query)
            else:
                if user in query.show_to.all():
                    newqueryset.append(query)
            

        serializer = self.get_serializer(newqueryset, many=True)
        return Response(serializer.data)
    
class SubItemperAssetViewSet(viewsets.ModelViewSet):
    queryset = SubItem_DBTable.objects.all()
    serializer_class = SubItemDBTableSerializer

    
    def list(self, request, *args, **kwargs):
        """
        Lista todos os elementos associados a um ativo específico.
        """
        params = request.query_params
        asset = params.get('Asset')

        # Validar se o parâmetro 'Asset' é um número válido
        if not asset or not asset.isdigit():
            return Response(
                {'message': 'Parâmetro Asset inválido. Deve ser um número inteiro.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Converter o parâmetro para inteiro
        asset_id = int(asset)

        company = request.user.companyId
        OBJasset = Asset_DBTable.objects.filter(pk=asset_id).first()

        if OBJasset and OBJasset.project.owner == company:
            queryset = self.get_queryset().filter(asset=asset_id)

            # Filtrar elementos ocultos
            for query in queryset:
                if query.is_ocult and request.user not in query.show_to.all():
                    queryset = queryset.exclude(pk=query.pk)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        # Caso o ativo não pertença à empresa do usuário
        return Response(
            {'message': 'Você não tem permissão para acessar esse ativo.'},
            status=status.HTTP_401_UNAUTHORIZED
        )



class AssetSubElementViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Sub_Element_Ativo_DBTable instances.

    :param queryset: The queryset that represents all Sub_Element_Ativo_DBTable instances.
    :type queryset: QuerySet
    :param serializer_class: The serializer class used to serialize and deserialize the Sub_Element_Ativo_DBTable instances.
    :type serializer_class: SubElementSerializer
    """
    queryset = Asset_Sub_Element_DBTable.objects.all()
    serializer_class = AssetSubElementSerializer

class imagesViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing images instances.

    :param queryset: The queryset that represents all images instances.
    :type queryset: QuerySet
    :param serializer_class: The serializer class used to serialize and deserialize the images instances.
    :type serializer_class: imagesSerializer
    """
    queryset = images.objects.all()
    serializer_class = imagesSerializer

    #define embed questionKey
    
    def list(self, request, *args, **kwargs):
        """
        List all images instances.

        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :param args: Additional arguments.
        :type args: list
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: HTTP response with the images instances.
        :rtype: rest_framework.response.Response

        :to use in front call the api with that example
        :use api.get('/api/images/',{params: {questionkey: 'questionkey'}})
        :The data that return is the images that have the questionkey
        :representated by that json
        :{
        :    "id": 1,
        :    "image": "image",
        :    "description": "description",
        :    "content_type": 1,
        :    "object_id": 1,
        :    "questionKey": "questionkey"
        :}
        """
        params = request.query_params
        if 'questionkey' in params:
            key = params.get('questionkey')
            contentType = params.get('content_type')
            object_id = params.get('object_id')

            if contentType == 'Asset':
                contentType = ContentType.objects.get_for_model(Asset_DBTable)
            if contentType == 'Element':
                contentType = ContentType.objects.get_for_model(SubItem_DBTable)
            if contentType == 'SubElement':
                contentType = ContentType.objects.get_for_model(Asset_Sub_Element_DBTable)
            queryset = self.get_queryset().filter(questionKey=key, content_type=contentType, object_id=object_id)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'Chave de pergunta não informada, informe a chave'}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def create(self, request, *args, **kwargs):
        """
        Create a new image instance.

        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :param args: Additional arguments.
        :type args: list
        :param kwargs: Additional keyword arguments.
        :type kwargs: dict
        :return: HTTP response with the image instance.
        :rtype: rest_framework.response.Response

        :to use in front call the api with that example
        :use api.post('/api/images/', {questionKey: 'questionkey', content_type: 'Asset', object_id: 1, image: 'image', description: 'description'})
        :The data that return is the image that have the questionkey

        """

        questionKey = request.data.get('questionKey')
        content_type = request.data.get('response_type')
        if content_type == 'Asset':
            content_type = ContentType.objects.get_for_model(Asset_DBTable)
        if content_type == 'Element':
            content_type = ContentType.objects.get_for_model(SubItem_DBTable)
        if content_type == 'SubElement':
            content_type = ContentType.objects.get_for_model(Asset_Sub_Element_DBTable)
        object_id = request.data.get('object_id')
        image = request.data.get('image')
        description = request.data.get('description')
        obj , create = images.objects.update_or_create(questionKey=questionKey, content_type=content_type, object_id=object_id, defaults={'image': image, 'description': description, 'questionKey': questionKey, 'content_type': content_type, 'object_id': object_id})
        return Response({'status': 'Image created successfully'}, status=status.HTTP_201_CREATED)
