from rest_framework import serializers
from Accounts.models import CustomUser_DBTable, Company_DBTable, Plans_DBTable
from django.contrib.auth import authenticate
from datetime import datetime

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)

    class Meta:
        model = CustomUser_DBTable
        fields = ['password']

class UserSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo de Usuário (CustomUser_DBTable).
    """
    class Meta:
        model = CustomUser_DBTable
        fields = '__all__'

class UserSerializerNoPassword(serializers.ModelSerializer):
    """
    Serializador de usuário sem incluir o campo de senha.
    """
    email = serializers.EmailField(required=True)
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField(required=True)
    birthDate = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d',])
    CPF = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    companyPosition = serializers.CharField(required=True)
    profileImage = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser_DBTable
        fields = ['email', 'firstName', 'lastName', 'birthDate', 'CPF', 'phone', 'companyPosition', 'profileImage']

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("email")
        password = data.get("password")

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("Usuário desativado.")
                data["user"] = user
            else:
                raise serializers.ValidationError("Credenciais inválidas.")
        else:
            raise serializers.ValidationError("Email e senha são obrigatórios.")
        return data

class CompanySerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo de Empresa (Company_DBTable).
    """
    user_Data = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = Company_DBTable
        fields = '__all__'

    def get_user_Data(self, obj):
        # Pega os dados dos usuários associados à empresa
        return [
            {
                'email': user['email'],
                'registrationDate': user['registrationDate'].strftime('%Y-%m-%d'),
                'lastConnection': user['lastConnection'].strftime('%Y-%m-%d')
            } 
            for user in obj.users.all().values('email', 'registrationDate', 'lastConnection')
        ]

    def get_user_email(self, obj):
        return [user.email for user in obj.users.all()]

class PlanSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo de Plano (Plans_DBTable).
    """
    class Meta:
        model = Plans_DBTable
        fields = '__all__'
