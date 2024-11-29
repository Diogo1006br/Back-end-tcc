from rest_framework import serializers, exceptions
from Accounts.models import CustomUser_DBTable
from Accounts.models import Company_DBTable
from Accounts.models import Plans_DBTable
from django.contrib.auth import authenticate
import datetime
# from .models import Account

class passwordSerializer(serializers.Serializer):

    password = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = CustomUser_DBTable
        fields = ['password']
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser_DBTable model.

    Fields:
        email (CharField): The email field of the user.
        password (CharField): The password field of the user.
    """
    class Meta:
        model = CustomUser_DBTable
        fields = '__all__'
class UserSerializerNoPassword(serializers.ModelSerializer):
    """
    Serializer for the CustomUser_DBTable model.
    """
    profileImage = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser_DBTable
        fields = ['profileImage']

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("email", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "Usuário está desativado."
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Não foi possível fazer login com as credenciais fornecidas."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Deve fornecer nome de usuário e senha."
            raise exceptions.ValidationError(msg)
        return data

from datetime import datetime

class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer for the Company_DBTable model.

    Fields:
        All fields of the Company_DBTable model are included.
    """
    user_Data = serializers.SerializerMethodField('get_user_Data')
    user_email = serializers.SerializerMethodField('get_user_email')

    class Meta:
        model = Company_DBTable
        fields = '__all__'

    def get_user_Data(self, obj):
        # Iterar sobre os objetos relacionados usando .all()
        userlist = []
        for user in obj.users.all().values('email', 'registrationDate', 'lastConnection'):
            registration_date = user['registrationDate']
            last_connection = user['lastConnection']

            # Converter os campos de data para string
            registration_date_str = registration_date.strftime('%Y-%m-%d') if isinstance(registration_date, datetime) else registration_date
            last_connection_str = last_connection.strftime('%Y-%m-%d') if isinstance(last_connection, datetime) else last_connection

            userdict = {
                'email': user['email'],
                'registrationDate': registration_date_str,
                'lastConnection': last_connection_str
            }
            userlist.append(userdict)

        return userlist
    
    def get_user_email(self, obj):
        user_email = [user.email for user in obj.users.all()]
        return user_email
    
    

class PlanSerializer(serializers.ModelSerializer):
    """
    Serializer for the Plans_DBTable model.

    Fields:
        All fields of the Plans_DBTable model are included.
    """
    class Meta:
        model = Plans_DBTable
        fields = '__all__'
