from rest_framework import viewsets
from django.conf import settings
from Projects.API.serializers import ProjectSerializer, ProjectSerializerOwnerWithNameAndNotID
from Projects.models import Project_DBTable
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from Accounts.models import CustomUser_DBTable
import datetime
import os
from django.core.files.storage import default_storage
from Utils.Mixins import Grupo_de_acesso_1Mixin, Grupo_de_acesso_3Mixin



# Create your views here.


class ProjectViewSet(viewsets.ModelViewSet):
    
    """
    View class for handling Projects.
    
    :param ModelViewSet: Base class for all views in the REST API that represent a collection of model instances.
    :type ModelViewSet: rest_framework.viewsets.ModelViewSet
    :ivar Projeto: Model class for Projects.
    :vartype Projeto: .models.Projeto
    :ivar ProjetoSerializer: Serializer class for Projects.
    :vartype ProjetoSerializer: .serializers.ProjetoSerializer

    :method list: Method to list all projects where user participates.
    :param request: HTTP request object.
    :type request: rest_framework.request.Request
    :return: HTTP response with a list of projects.
    :rtype: rest_framework.response.Response

    :method create: Method to create a new project.
    :param request: HTTP request object.
    :type request: rest_framework.request.Request
    :return: HTTP response with the data of the created project if creation is successful, otherwise an error message.
    :rtype: rest_framework.response.Response

    :method update: Method to update an existing project.
    :param request: HTTP request object.
    :type request: rest_framework.request.Request
    :return: HTTP response with the data of the updated project if the update is successful, otherwise an error message.
    :rtype: rest_framework.response.Response
    """
    queryset = Project_DBTable.objects.all()
    serializer_class = ProjectSerializer
    def send_html_email(self, to_list, subject, template_name, context, from_email=None):
        print('CHEGUEI NA FUNÇÃO....')
        html_content = render_to_string(template_name, context)  # renderiza o template HTML com o contexto
        email = EmailMessage(subject, html_content, from_email, to_list)
        email.content_subtype = "html"  # Define o conteúdo do e-mail como HTML
        email.send()
        print('EMAIL ENVIADO....')  # envia o e-mail

    @method_decorator(login_required)
    def list(self, request):
        """
        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :return: HTTP response with a list of projects.
        :rtype: rest_framework.response.Response

        :Request: GET /api url/projects/
        """
        mixin = Grupo_de_acesso_1Mixin()
        if mixin.test_func(request) == True:
            queryset = self.get_queryset().filter(members=request.user)
            serializer = ProjectSerializerOwnerWithNameAndNotID(queryset, many=True)
            return Response(serializer.data)


    @method_decorator(login_required)        
    def create(self, request, *args, **kwargs):
        mixin = Grupo_de_acesso_3Mixin()
        if mixin.test_func(request) == True:
            data = request.POST.copy()
            files = request.FILES
            data['image'] = files.get('image', None)
            members_data = data.getlist('members[]')
            if members_data == []:
                return Response({'error': 'Informe os membros'}, status=status.HTTP_400_BAD_REQUEST)
            image = data.get('image', None)
            if image is None or image == '' or image == 'undefined' or image == 'null':
                if settings.DEBUG:
                    image ='/projects_images/default.jpg'
                if settings.DEBUG == False:
                    file_path = 'projects_images/default.jpg'
                    if default_storage.exists(file_path):
                        image=default_storage.url(file_path)
                    else:
                        image = None

            newData = {'projectName': data.get('projectName', ''),
                        'projectDescription': data.get('projectDescription', ''),
                        'image': image,
                        'owner': request.user.companyId,
                        'user_has_created': request.user,
                        'user_has_modified': request.user,
                        }
                            
            try:
                valid_Members = []
                for email in members_data:
                    print(f'Email: {email}')  # Imprimir o email
                    try:
                        get_user_model().objects.get(email=email)
                        if get_user_model().objects.filter(email=email).exists():
                            valid_Members.append(email)
                    except get_user_model().DoesNotExist:
                        context = {'email': email,
                        'Inviter':request.user.email,
                        'projectName':data.get('projectName',''),}
                        self.send_html_email([email], 'Invite Aria-IO', 'Invite.html', context,settings.EMAIL_HOST_USER)

                project = Project_DBTable.objects.create(**newData)
                project.save()
                project.members.set(CustomUser_DBTable.objects.filter(email__in=valid_Members))
                return Response({'message': 'Projeto criado com sucesso'}, status=status.HTTP_201_CREATED)

            except ValidationError as e:
                print(e)
                return Response(e, status=status.HTTP_400_BAD_REQUEST)
            
        
            
            



    
    @method_decorator(login_required)
    def update(self, request, *args, **kwargs):
        mixin = Grupo_de_acesso_3Mixin()
        if mixin.test_func(request) == True:
            data = request.POST.copy()
            instance = self.get_object()
            members_data = data.getlist('members[]')
            files = request.FILES
            data['image'] = files.get('image', None)
            image = data.get('image', None)
            if image is None or image == '' or image == 'undefined' or image == 'null':
                if settings.DEBUG:
                    image = '/projects_images/default.jpg'
                else:
                    file_path = 'projects_images/default.jpg'
                    if default_storage.exists(file_path):
                        image = default_storage.url(file_path)
                    else:
                        image = None
            if members_data == []:
                return Response({'error': 'Informe os membros'}, status=status.HTTP_400_BAD_REQUEST)

            newData = {
                'projectName': data.get('projectName', ''),
                'projectDescription': data.get('projectDescription', ''),
                'image': image,
                'owner': request.user.companyId,
                'user_has_created': request.user,
                'user_has_modified': request.user,
            }

            try:
                valid_Members = []
                for email in members_data:
                    print(f'Email: {email}')  # Imprimir o email
                    try:
                        get_user_model().objects.get(email=email)
                        if get_user_model().objects.filter(email=email).exists():
                            valid_Members.append(email)
                    except get_user_model().DoesNotExist:
                        context = {
                            'email': email,
                            'Inviter': request.user.email,
                            'projectName': data.get('projectName', ''),
                        }
                        self.send_html_email([email], 'Invite Aria-IO', 'Invite.html', context, settings.EMAIL_HOST_USER)

                # Atualizar o projeto
                Project_DBTable.objects.filter(id=instance.id).update(**newData)
                # Buscar o projeto atualizado
                project = Project_DBTable.objects.get(id=instance.id)

                # Atribuir os membros ao projeto
                project.members.set(CustomUser_DBTable.objects.filter(email__in=valid_Members))
                project.image = image
                project.save()

                return Response({'message': 'Projeto atualizado com sucesso'}, status=status.HTTP_200_OK)

            except ValidationError as e:
                print(e)
                return Response(e, status=status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(login_required)
    def destroy(self, request, *args, **kwargs):
        """
        Deletes a project.

        :param request: HTTP request object.
        :type request: rest_framework.request.Request
        :return: HTTP response with a success message if the project is successfully deleted, otherwise an error message.
        :rtype: rest_framework.response.Response

        :Request: DELETE /api url/projects/{id}/
        """
        mixin = Grupo_de_acesso_3Mixin()
        if mixin.test_func(request) == True:
            try:
                # Obter o objeto existente
                instance = self.get_object()

                if instance.image:
                    # alterar este delete quan for para produção
                    file_path = os.path.join(settings.MEDIA_ROOT, str(instance.image))

                    # Verificar se o arquivo existe
                    if os.getenv('DEBUG') == 'True':
                        if os.path.isfile(file_path):
                            # Deletar o arquivo
                            os.remove(file_path)
                    if os.getenv('DEBUG') == 'False':
                    
                        file_path = str(instance.image)

                
                        if default_storage.exists(file_path):
                            # Deletar o arquivo
                            default_storage.delete(file_path)
                    


            
                # Deletar o objeto
                instance.delete()
            except ObjectDoesNotExist:
                return Response({'error': 'Projeto não encontrado'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'message': 'Projeto deletado com sucesso'}, status=status.HTTP_200_OK)



    
