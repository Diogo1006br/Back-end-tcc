from rest_framework import viewsets, status
from rest_framework.response import Response
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.files.storage import default_storage
from django.core.exceptions import ObjectDoesNotExist
import os

from Projects.API.serializers import ProjectSerializer, ProjectSerializerOwnerWithNameAndNotID
from Projects.models import Project_DBTable
from Accounts.models import CustomUser_DBTable, Company_DBTable
from Utils.Mixins import Grupo_de_acesso_1Mixin, Grupo_de_acesso_3Mixin

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project_DBTable.objects.all()
    serializer_class = ProjectSerializer

    def send_html_email(self, to_list, subject, template_name, context, from_email=None):
        html_content = render_to_string(template_name, context)
        email = EmailMessage(subject, html_content, from_email, to_list)
        email.content_subtype = "html"
        email.send()

    def list(self, request):
        queryset = self.get_queryset().filter(members=1)
        serializer = ProjectSerializerOwnerWithNameAndNotID(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
            members_data = request.data.getlist('members[]')
            if not members_data:
                return Response({'error': 'Informe os membros'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Preparar os dados do projeto
                newData = self._prepare_project_data(request)
                # Validar os membros
                valid_members = self._validate_members(members_data, request, newData['projectName'])
                # Criar o projeto
                project = Project_DBTable.objects.create(**newData)
                project.members.set(CustomUser_DBTable.objects.filter(email__in=valid_members))
                return Response({'message': 'Projeto criado com sucesso'}, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': 'Erro interno ao criar o projeto', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def update(self, request, *args, **kwargs):
        mixin = Grupo_de_acesso_3Mixin()
        if mixin.test_func(request):  # Passando request aqui
            instance = self.get_object()
            members_data = request.data.getlist('members[]')
            if not members_data:
                return Response({'error': 'Informe os membros'}, status=status.HTTP_400_BAD_REQUEST)

            newData = self._prepare_project_data(request)
            valid_members = self._validate_members(members_data, request, newData['projectName'])

            for attr, value in newData.items():
                setattr(instance, attr, value)
            instance.save()
            instance.members.set(CustomUser_DBTable.objects.filter(email__in=valid_members))
            return Response({'message': 'Projeto atualizado com sucesso'}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.image:
            file_path = os.path.join(settings.MEDIA_ROOT, str(instance.image))
            if settings.DEBUG and os.path.isfile(file_path):
                os.remove(file_path)

            instance.delete()
            return Response({'message': 'Projeto deletado com sucesso'}, status=status.HTTP_204_NO_CONTENT)

    def _prepare_project_data(self, request):
        data = request.data.copy()
        image = data.get('image', None)
        if not image or image in ('', 'undefined', 'null'):
            image = '/projects_images/default.jpg' if settings.DEBUG else self.get_default_image()

        mock_company = Company_DBTable(
            id=2,
            companyName="Test Company ",
            CNPJ="12.345.678/0001-90",
            address="Rua Teste, 123",
            city="Cidade Teste",
            state="São Paulo"
        )

        mocked_user = CustomUser_DBTable(
            id=1,  # Use um ID de usuário existente ou um fictício
            email="mockuser@test.com",
            firstName="Mock",
            companyId=mock_company
        )

        return {
            'projectName': data.get('projectName', ''),
            'projectDescription': data.get('projectDescription', ''),
            'image': image,
            'owner': mock_company,
            'user_has_created': mocked_user,
            'user_has_modified': mocked_user,
        }

    def _validate_members(self, members_data, request, project_name):
        valid_members = []
        for email in members_data:
            if get_user_model().objects.filter(email=email).exists():
                valid_members.append(email)
            else:
                context = {
                    'email': email,
                    'Inviter': request.user.email,
                    'projectName': project_name,
                }
                self.send_html_email([email], 'Invite UF-IO', 'Invite.html', context, settings.EMAIL_HOST_USER)
        return valid_members

    def get_default_image(self):
        file_path = 'projects_images/default.jpg'
        if default_storage.exists(file_path):
            return default_storage.url(file_path)
        return None
