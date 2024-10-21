from rest_framework import serializers
from Forms.models import Form, FormResponse,DropboxAnswerList
from django.contrib.contenttypes.models import ContentType
from Registrations.models import Asset_DBTable, SubItem_DBTable, Asset_Sub_Element_DBTable


class FormSerializer(serializers.ModelSerializer):
    """
    A serializer for the Form model.

    :param Meta: The metadata for the serializer.
    :type Meta: class
    :param model: The model that the serializer is for.
    :type model: Form
    :param fields: The fields to include in the serialized representation.
    :type fields: str
    """
    class Meta:
        model = Form
        fields = '__all__'

class Form_ResponseSerializer(serializers.ModelSerializer):
    """
    A serializer for the FormResponse model.

    :param Meta: The metadata for the serializer.
    :type Meta: class
    :param model: The model that the serializer is for.
    :type model: FormResponse
    :param fields: The fields to include in the serialized representation.
    :type fields: str
    """

    class Meta:
        model = FormResponse
        fields = '__all__'
            # Faça algo para o caso de 'SUBELEMENT'


   

class DropboxAnswerListSerializer(serializers.ModelSerializer):
    """
    A serializer for the DropboxAnswerList model.

    :param Meta: The metadata for the serializer.
    :type Meta: class
    :param model: The model that the serializer is for.
    :type model: DropboxAnswerList
    :param fields: The fields to include in the serialized representation.
    :type fields: str
    """
    class Meta:
        model = DropboxAnswerList
        fields = '__all__'

class DropboxAnserListSerializerCompanyNameListing(serializers.ModelSerializer):
    """
    A serializer for the DropboxAnswerList model.

    :param Meta: The metadata for the serializer.
    :type Meta: class
    :param model: The model that the serializer is for.
    :type model: DropboxAnswerList
    :param fields: The fields to include in the serialized representation.
    :type fields: str
    """
    company = serializers.SerializerMethodField()
    class Meta:
        model = DropboxAnswerList
        fields = '__all__'
    def get_company(self, obj):
        return obj.company.companyName