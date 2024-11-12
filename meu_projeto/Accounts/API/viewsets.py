from rest_framework import viewsets, status
from rest_framework.response import Response
from Accounts.API import serializers
from Accounts.models import Company_DBTable, CustomUser_DBTable
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.conf import settings
from Utils.Mixins import Grupo_de_acesso_3Mixin

# Importa o serializer corrigido
from Accounts.API.serializers import UserSerializerNoPassword


class PasswordViewSet(viewsets.ViewSet):
    @method_decorator(login_required)
    def update(self, request, pk=None):
        user = request.user
        serializer = serializers.passwordSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CompanySerializer
    queryset = Company_DBTable.objects.all()

    @method_decorator(login_required)
    def list(self, request):
        company = request.user.companyId
        serializer = serializers.CompanySerializer(company)
        return Response(serializer.data)

    @method_decorator(login_required)
    def update(self, request, pk=None):
        mixin = Grupo_de_acesso_3Mixin()
        if not mixin.test_func(request):
            return mixin.handle_no_permission()
        
        data = request.data.copy()
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
        
        Company_DBTable.objects.filter(id=instance.id).update(**newData)
        
        company = Company_DBTable.objects.get(id=instance.id)
        company.users.set(valid_Members)
        company.logotipo = image
        
        try:
            company.save()
            return Response({'message': 'Empresa atualizada com sucesso'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Erro ao atualizar a empresa'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = CustomUser_DBTable.objects.all()

    @method_decorator(login_required)
    def create(self, request, *args, **kwargs):
        userGroup = request.user.groups.all()[0].name
        if 'Gestor da empresa' in userGroup or 'Admins' in userGroup:
            if 'is_staff' in request.data:
                request.data['is_staff'] = False
                request.data['is_superuser'] = False
            return super().create(request, *args, **kwargs)
        else:
            return Response({'message': 'Você não tem permissão para criar um novo usuário'}, status=status.HTTP_401_UNAUTHORIZED)


class ReturnLogedUser(viewsets.ViewSet):
    @method_decorator(login_required)
    def list(self, request):
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
        user = request.user
        serializer = UserSerializerNoPassword(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
