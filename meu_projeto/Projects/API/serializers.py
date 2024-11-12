from rest_framework import serializers
from django.contrib.auth import get_user_model
from Projects.models import Project_DBTable
from Accounts.models import CustomUser_DBTable
from django.contrib.auth import authenticate
import datetime

class ProjectSerializerOwnerWithNameAndNotID(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField('get_owner_name')

    class Meta:
        model = Project_DBTable
        fields = '__all__'

    def get_owner_name(self, obj):
        return obj.owner.companyName

class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Project model.

    This class is used to serialize and deserialize Project instances into Python datatypes. It inherits from Django Rest Framework's ModelSerializer.

    :param serializers.ModelSerializer: Base class for model serializers.
    :type serializers.ModelSerializer: rest_framework.serializers.ModelSerializer

    :ivar members: A field that represents the members of the project. It uses a SlugRelatedField to represent the members by their email.
    :vartype members: rest_framework.serializers.SlugRelatedField

    :ivar Meta: A class that contains metadata for the serializer.
    :vartype Meta: class

    Methods
    -------
    None
    """

    members = serializers.SlugRelatedField(
        many=True,
        queryset=CustomUser_DBTable.objects.all(),
        slug_field='email'
    )

    user_Data = serializers.SerializerMethodField('get_user_Data')

    class Meta:
        """
        A class that contains metadata for the serializer.

        :param model: The model that the serializer is for.
        :type model: Project_DBTable
        :param fields: The fields to include in the serialized representation.
        :type fields: str
        """
        model = Project_DBTable
        fields = '__all__'

    def get_user_Data(self, obj):
        """
        A method that returns the user data for a given project.

        :param obj: The project to get the user data for.
        :type obj: Project_DBTable
        :return: The user data for the project.
        :rtype: dict
        """

        userlist = []
        for user in obj.members.all().values('email', 'registrationDate', 'lastConnection', 'companyId__companyName'):
            registration_date = user['registrationDate']
            last_connection = user['lastConnection']

            # Converter os campos de data para string
            registration_date_str = registration_date.strftime('%Y-%m-%d') if isinstance(registration_date, (datetime.date, datetime.datetime)) else registration_date
            last_connection_str = last_connection.strftime('%Y-%m-%d') if isinstance(last_connection, (datetime.date, datetime.datetime)) else last_connection

            userdict = {
                'email': user['email'],
                'registrationDate': registration_date_str,
                'lastConnection': last_connection_str,
                'company': user['companyId__companyName']
            }
            userlist.append(userdict)

        return userlist