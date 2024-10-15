from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
class Form(models.Model):
    """
    A Form is a model that represents a form with fields that can be filled out by users.

    :param name: The name of the form.
    :type name: models.CharField
    :param form: The fields of the form in JSON format.
    :type form: models.JSONField
    :param created_at: The date and time the form was created.
    :type created_at: models.DateTimeField
    :param updated_at: The date and time the form was last updated.
    :type updated_at: models.DateTimeField
    :param company: The company that owns the form.
    :type company: models.ForeignKey
    :return: The name of the form.
    :rtype: str
    """
    name = models.CharField(max_length=255, default='formulario default')
    form = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey('Accounts.Company_DBTable', on_delete=models.CASCADE)
    choices = (
        ('Arquivado','Arquivado'),
        ('Ativo','Ativo'),
    )
    status = models.CharField('Status',max_length=100,choices=choices,default='Ativo')
    def __str__(self):
        return self.name

class FormResponse(models.Model):
    """
    A FormResponse is a model that represents a user's response to a form.

    :param formID: The form that the response is associated with.
    :type formID: models.ForeignKey
    :param response: The user's response to the form in JSON format.
    :type response: models.JSONField
    :param created_at: The date and time the response was created.
    :type created_at: models.DateTimeField
    :param updated_at: The date and time the response was last updated.
    :type updated_at: models.DateTimeField
    :param content_type: The type of content in the response.
    :type content_type: models.ForeignKey
    :param object_id: The ID of the related object.
    :type object_id: models.PositiveIntegerField
    :param Instancia: The instance of the related object.
    :type Instancia: GenericForeignKey
    :return: The name of the form associated with the response.
    :rtype: str
    """
    formID = models.ForeignKey(Form, on_delete=models.CASCADE)
    response = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    Instance = GenericForeignKey('content_type', 'object_id')
    
    def __str__(self):
        return self.formID.name
    
class DropboxAnswerList(models.Model):
        #2 campos list e form
        """
        A DropboxAnswerList is a model that represents a list of answers to a form field.

        :param list: The list of answers in JSON format.
        :type list: models.JSONField
        :param project: The project that the list of answers is associated with.
        :type form: models.ForeignKey
        :return: The list of answers.
        :rtype: list
        """
        name = models.CharField(max_length=255, null=True)
        list = models.JSONField()
        company = models.ForeignKey('Accounts.Company_DBTable', on_delete=models.CASCADE, null=True)

        def __str__(self):
            return self.name
       