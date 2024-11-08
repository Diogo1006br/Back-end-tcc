from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q
from .serializers import AssetDBTableSerializer, SubItemDBTableSerializer, AssetSubElementSerializer, imagesSerializer, ActionDBTableSerializer, CommentSerializer, AssetDBTableSerializerwithformname
from Registrations.models import Asset_DBTable, SubItem_DBTable, Asset_Sub_Element_DBTable, images, Action_DBTable, Comment_DBTable
from django.contrib.contenttypes.models import ContentType
from Projects.models import Project_DBTable
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from Accounts.models import CustomUser_DBTable
from Utils.Mixins import Grupo_de_acesso_3Mixin, Grupo_de_acesso_1Mixin, Grupo_de_acesso_2Mixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment_DBTable.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        mixin = Grupo_de_acesso_2Mixin()
        mixin.request = request
        if not mixin.test_func():
            return mixin.handle_no_permission()
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
        obj, create = Comment_DBTable.objects.update_or_create(comment=comment, content_type=content_type, object_id=object_id, user=user, questionKey=questionKey)
        return Response({'status': 'Comment created successfully'}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        mixin = Grupo_de_acesso_1Mixin()
        mixin.request = request
        if not mixin.test_func():
            return mixin.handle_no_permission()
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

class ActionViewSet(viewsets.ModelViewSet):
    def send_html_email(self, to_list, subject, template_name, context, from_email=None):
        print('CHEGUEI NA FUNÇÃO....')
        html_content = render_to_string(template_name, context)
        email = EmailMessage(subject, html_content, from_email, to_list)
        email.content_subtype = "html"
        email.send()
        print('EMAIL ENVIADO....')

    queryset = Action_DBTable.objects.all()
    serializer_class = ActionDBTableSerializer

    @method_decorator(login_required)
    def list(self, request, *args, **kwargs):
        mixin = Grupo_de_acesso_2Mixin()
        mixin.request = request
        if not mixin.test_func():
            return mixin.handle_no_permission()
        request_user = request.user
        queryset = super().get_queryset().filter(Q(responsible=request_user) | Q(user_hasCreated=request_user))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @method_decorator(login_required)
    def create(self, request, *args, **kwargs):
        mixin = Grupo_de_acesso_2Mixin()
        mixin.request = request
        if not mixin.test_func():
            return mixin.handle_no_permission()
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
            context = {'email': user_email, 'Inviter': request.user.email, 'title': title}
            self.send_html_email([user_email], 'Invite IF', 'Invite.html', context, settings.EMAIL_HOST_USER)

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
    queryset = Asset_DBTable.objects.all()
    serializer_class = AssetDBTableSerializer

    @method_decorator(login_required)
    def list(self, request, *args, **kwargs):
        mixin = Grupo_de_acesso_1Mixin()
        mixin.request = request
        if not mixin.test_func():
            return mixin.handle_no_permission()
        params = request.query_params

        if 'project' in params:
            projeto = params.get('project')
            OBJproject = Project_DBTable.objects.filter(pk=projeto).first()
            if OBJproject and OBJproject.owner == request.user.companyId:
                queryset = self.get_queryset().filter(project=projeto)
                serializer = AssetDBTableSerializerwithformname(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Você não tem permissão para acessar esse projeto'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            user = request.user
            projects = Project_DBTable.objects.filter(members=user)
            queryset = self.get_queryset().filter(project__in=projects)
            serializer = AssetDBTableSerializerwithformname(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(login_required)
    def create(self, request, *args, **kwargs):
        mixin = Grupo_de_acesso_2Mixin()
        mixin.request = request
        if not mixin.test_func():
            return mixin.handle_no_permission()
        data = request.data
        try:
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            return Response({'status': 'Asset not created', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)    
        return Response({'status': 'Asset created successfully'},)

    @method_decorator(login_required)
    def destroy(self, request, *args, **kwargs):
        mixin = Grupo_de_acesso_3Mixin()
        mixin.request = request
        if not mixin.test_func():
            return Response(status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        subItems = SubItem_DBTable.objects.filter(ativo=instance.id)
        try:
            for item in subItems:
                item.delete()
            instance.delete()
            return Response({'status': 'Asset deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'status': 'Error deleting asset', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SubItemDBTableViewSet(viewsets.ModelViewSet):
    queryset = SubItem_DBTable.objects.all()
    serializer_class = SubItemDBTableSerializer

    @method_decorator(login_required)
    def list(self, request, *args, **kwargs):
        mixin = Grupo_de_acesso_1Mixin()
        mixin.request = request
        if not mixin.test_func():
            return mixin.handle_no_permission()
        user = request.user
        projetos = Project_DBTable.objects.filter(members=user)
        assets =  Asset_DBTable.objects.filter(project__in=projetos)
        queryset = self.get_queryset().filter(asset__in=assets)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class SubItemperAssetViewSet(viewsets.ModelViewSet):
    queryset = SubItem_DBTable.objects.all()
    serializer_class = SubItemDBTableSerializer

    @method_decorator(login_required)
    def list(self, request, *args, **kwargs):
        mixin = Grupo_de_acesso_1Mixin()
        mixin.request = request
        if not mixin.test_func():
            return mixin.handle_no_permission()
        params = request.query_params
        company = request.user.companyId
        if 'Asset' in params:
            asset = params.get('Asset')
            OBJasset = Asset_DBTable.objects.filter(pk=asset).first()
            if OBJasset.project.owner == company:
                queryset = self.get_queryset().filter(asset=asset)
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({'message': 'Você não tem permissão para acessar esse ativo'}, status=status.HTTP_401_UNAUTHORIZED)

class AssetSubElementViewSet(viewsets.ModelViewSet):
    queryset = Asset_Sub_Element_DBTable.objects.all()
    serializer_class = AssetSubElementSerializer

class imagesViewSet(viewsets.ModelViewSet):
    queryset = images.objects.all()
    serializer_class = imagesSerializer

    @method_decorator(login_required)
    def list(self, request, *args, **kwargs):
        mixin = Grupo_de_acesso_1Mixin()
        mixin.request = request
        if not mixin.test_func():
            return mixin.handle_no_permission()
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

    @method_decorator(login_required)
    def create(self, request, *args, **kwargs):
        mixin = Grupo_de_acesso_2Mixin()
        mixin.request = request
        if not mixin.test_func():
            return mixin.handle_no_permission()
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
