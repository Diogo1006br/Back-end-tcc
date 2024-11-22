from rest_framework import serializers
from Registrations.models import Asset_DBTable,SubItem_DBTable,Asset_Sub_Element_DBTable,images,Action_DBTable,Comment_DBTable

class CommentSerializer(serializers.ModelSerializer):
    """
    A serializer for the comment model.

    :param Meta: The metadata for the serializer.
    :type Meta: class
    :param model: The model that the serializer is for.
    :type model: comment
    :param fields: The fields to include in the serialized representation.
    :type fields: str
    """
    user_email = serializers.SerializerMethodField()
    class Meta:
        model = Comment_DBTable
        fields = '__all__'
    def get_user_email(self, obj):
        return obj.user.email
class ActionDBTableSerializer(serializers.ModelSerializer):
    """
    A serializer for the action_DBTable model.

    :param Meta: The metadata for the serializer.
    :type Meta: class
    :param model: The model that the serializer is for.
    :type model: action_DBTable
    :param fields: The fields to include in the serialized representation.
    :type fields: str
    """
    responsible_email = serializers.SerializerMethodField()
    instance_name = serializers.SerializerMethodField()
    user_hasCreated_email = serializers.SerializerMethodField()
    class Meta:
        model = Action_DBTable
        fields = '__all__'

    def get_responsible_email(self, obj):
        return obj.responsible.email
    def get_user_hasCreated_email(self, obj):
        return obj.user_hasCreated.email
    def get_instance_name(self, obj):
        try:
            return obj.Instance.assetName
        except:
            return obj.Instance.elementName
        
class AssetDBTableSerializerwithformname(serializers.ModelSerializer):
    """
    A serializer for the Asset_DBTable model.

    :param Meta: The metadata for the serializer.
    :type Meta: class
    :param model: The model that the serializer is for.
    :type model: Asset_DBTable
    :param fields: The fields to include in the serialized representation.
    :type fields: str
    """
    form_name = serializers.SerializerMethodField()

    class Meta:
        model = Asset_DBTable
        fields = ['id','assetName', 'form', 'form_name', 'project','status','show_to']

    def get_form_name(self, obj):
        return obj.form.name
class AssetDBTableSerializer(serializers.ModelSerializer):
    form_name = serializers.SerializerMethodField()

    class Meta:
        model = Asset_DBTable
        fields = ['id','assetName', 'form', 'form_name', 'project','status', 'is_ocult', 'show_to'] # adicionar show_to quando fizer o inputtag no frontend

    def get_form_name(self, obj):
        return obj.form.name

class SubItemDBTableSerializer(serializers.ModelSerializer):
    """
    A serializer for the Element_Ativo_DBTable model.

    :param Meta: The metadata for the serializer.
    :type Meta: class
    :param model: The model that the serializer is for.
    :type model: Element_Ativo_DBTable
    :param fields: The fields to include in the serialized representation.
    :type fields: str
    """
    form_name = serializers.SerializerMethodField()
    class Meta:
        model = SubItem_DBTable
        fields = '__all__'
    def get_form_name(self, obj):
        return obj.form.name
class AssetSubElementSerializer(serializers.ModelSerializer):
    """
    A serializer for the Sub_Element_Ativo_DBTable model.

    :param Meta: The metadata for the serializer.
    :type Meta: class
    :param model: The model that the serializer is for.
    :type model: Sub_Element_Ativo_DBTable
    :param fields: The fields to include in the serialized representation.
    :type fields: str
    """
    class Meta:
        model = Asset_Sub_Element_DBTable
        fields = '__all__'

class imagesSerializer(serializers.ModelSerializer):
    """
    A serializer for the images model.

    :param Meta: The metadata for the serializer.
    :type Meta: class
    :param model: The model that the serializer is for.
    :type model: images
    :param fields: The fields to include in the serialized representation.
    :type fields: str
    """
    class Meta:
        model = images
        fields = '__all__'