from rest_framework import viewsets
from Accounts.API import serializers
from Accounts.models import Company_DBTable, CustomUser_DBTable
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.conf import settings
from Utils.Mixins import Grupo_de_acesso_3Mixin  # Import the mixin

class PasswordViewSet(viewsets.ViewSet):
    """
    View class for password data.
    """
    @method_decorator(login_required)
    def update(self, request, pk=None):
        """
        Method to update the password of a user.

        Args:
            request (rest_framework.request.Request): The request object.
            pk (int): The primary key of the user.

        Returns:
            rest_framework.response.Response: The updated user data.

        """
        user = request.user
        serializer = serializers.passwordSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyViewSet(viewsets.ModelViewSet):
    """
    View class for company data.

    Attributes:
        serializer_class (CompanySerializer): Serializer for the company data.
        queryset (QuerySet): Queryset that includes all objects of the Company_DBTable model.
    """
    serializer_class = serializers.CompanySerializer
    queryset = Company_DBTable.objects.all()

    @method_decorator(login_required)
    def list(self, request):
        """
        Method to list the company of the logged-in user.

        Args:
            request (rest_framework.request.Request): The request object.

        Returns:
            rest_framework.response.Response: The company data of the logged-in user.

        """
        company = request.user.companyId
        serializer = serializers.CompanySerializer(company)
        return Response(serializer.data)

    @method_decorator(login_required)
    def update(self, request, pk=None):
        """
        Method to update a company.

        Args:
            request (rest_framework.request.Request): The request object.
            pk (int): The primary key of the company.

        Returns:
            rest_framework.response.Response: The updated company data.

        """
        mixin = Grupo_de_acesso_3Mixin()
        if not mixin.test_func(request):
            return mixin.handle_no_permission()
        
        data = request.data.copy()  # Create a mutable copy of the data
        files = request.FILES
        data['logotipo'] = files.get('logotipo', None)
        image = data.get('image', None)
        
        if not image or image in ['undefined', 'null']:
            if settings.DEBUG:
                image = '/projects_images/default.jpg'
            else:
                file_path = 'projects_images/default.jpg'
                if default_storage.exists(file_path):
                    image = default_storage.url(file_path)
                else:
                    image = None

        instance = self.get_object()
        members_data = data.getlist('user_email[]')
        valid_Members = []
        for email in members_data:
            try:
                user = get_user_model().objects.get(email=email)
                valid_Members.append(user)
            except get_user_model().DoesNotExist:
                return Response({'message': 'O email não existe'}, status=status.HTTP_400_BAD_REQUEST)

        newData = {
            'companyName': data['companyName'],
            'CNPJ': data['CNPJ'],
            'address': data['address'],
            'telephone': data['telephone'],
            'comercialEmail': data['comercialEmail'],
            'site': data['site'],
        }
        
        # Update the company
        Company_DBTable.objects.filter(id=instance.id).update(**newData)
        
        # Fetch updated company
        company = Company_DBTable.objects.get(id=instance.id)
        
        # Set company members
        company.users.set(valid_Members)
        company.logotipo = image
        
        try:
            company.save()
            return Response({'message': 'Empresa atualizada com sucesso'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Erro ao atualizar a empresa'}, status=status.HTTP_400_BAD_REQUEST)
        

class UserViewSet(viewsets.ModelViewSet):
    """
    View class for user data.

    Attributes:
        serializer_class (UserSerializer): Serializer for the user data.
        queryset (QuerySet): Queryset that includes all objects of the CustomUser_DBTable model.
    """
    serializer_class = serializers.UserSerializer
    queryset = CustomUser_DBTable.objects.all()

    @method_decorator(login_required)
    def create(self, request, *args, **kwargs):
        """
        Method to create a new user.

        Args:
            request (rest_framework.request.Request): The request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            rest_framework.response.Response: HTTP response with the new user data if the user was created successfully, otherwise an error message.

        Raises:
            HTTP_401_UNAUTHORIZED: If the user is not part of the 'Gestor da empresa' or 'Admins' groups.
        """
        userGroup = request.user.groups.all()[0].name

        if 'Gestor da empresa' in userGroup or 'Admins' in userGroup:
            if 'is_staff' in request.data:
                request.data['is_staff'] = False
                request.data['is_superuser'] = False
                
            return super().create(request, *args, **kwargs)
        else:
            return Response({'message': 'Você não tem permissão para criar um novo usuário'}, status=status.HTTP_401_UNAUTHORIZED)


class ReturnLogedUser(viewsets.ViewSet):
    """
    View class to return information about the currently logged in user.
    """
    @method_decorator(login_required)
    def list(self, request):
        """
        Method to return information about the currently logged in user.

        Args:
            request (rest_framework.request.Request): The request object.

        Returns:
            rest_framework.response.Response: The currently logged in user.

        """
        user = request.user
        user_dict = {
            "id": user.id,
            "email": user.email,
            "company": user.companyId.companyName,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "companyPosition": user.companyPosition,
            "CPF": user.CPF,
            "phone": user.phone,
            "birthDate": user.birthDate,
            "profileImage": '',
        }
        
        if user.profileImage:
            user_dict['profileImage'] = user.profileImage.url
        
        return Response(user_dict)

    @method_decorator(login_required)
    def update(self, request, pk=None):
        """
        Method to update the currently logged in user.

        Args:
            request (rest_framework.request.Request): The request object.
            pk (int): The primary key of the user.

        Returns:
            rest_framework.response.Response: The updated user data.

        """
        user = request.user
        serializer = UserSerializerNoPassword(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
