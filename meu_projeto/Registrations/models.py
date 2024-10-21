from django.db import models

# Create your models here.
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Asset_DBTable(models.Model):

    assetName = models.CharField('Nome do ativo', max_length=100)
    form = models.ForeignKey('Forms.Form', on_delete= models.CASCADE)
    project = models.ForeignKey('Projects.Project_DBTable',on_delete=models.CASCADE, null=True)
    options = (
        ('Ativo','Ativo'),
        ('Arquivado','Arquivado'),
    )
    status = models.CharField('Status',max_length=100,choices=options,default='Ativo')
    def __str__(self):

            return self.assetName
class SubItem_DBTable(models.Model):
    elementName = models.CharField('nome do elemento',max_length=100)
    asset = models.ForeignKey('Asset_DBTable',on_delete=models.CASCADE)
    form = models.ForeignKey('Forms.Form', on_delete=models.CASCADE)
    def __str__(self):
        return self.elementName
class Asset_Sub_Element_DBTable(models.Model):
    nameSubElement = models.CharField('nome do subElemento', max_length=100)
    element = models.ForeignKey('SubItem_DBTable',on_delete=models.CASCADE)
    form = models.ForeignKey('Forms.Form', on_delete=models.CASCADE)
    def __str__(self):
        return self.nameSubElement

class images(models.Model):
    image = models.ImageField(verbose_name='Foto',upload_to='ativos/')

    description = models.TextField(verbose_name='Descrição',max_length=2000,null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='Ativo ou Elemento')
    # O campo object_id armazena o ID do objeto relacionado
    object_id = models.PositiveIntegerField(verbose_name='ID do Ativo/Elemento?')
    Instance = GenericForeignKey('content_type', 'object_id')
    questionKey = models.CharField('Chave da pergunta',max_length=100,null=True)

class Action_DBTable(models.Model):
    title = models.CharField('Nome da ação',max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='Ativo ou Elemento')
    object_id = models.PositiveIntegerField(verbose_name='ID do Ativo/Elemento?')
    Instance = GenericForeignKey('content_type', 'object_id')
    choices = (
        ('Baixa','Baixa'),
        ('Media','Media'),
        ('Alta','Alta'),
    )
    priority = models.CharField('Prioridade',max_length=100,choices=choices)

    deadline = models.DateField('Data limite',null=True)

    responsible = models.ForeignKey('Accounts.CustomUser_DBTable',on_delete=models.CASCADE,related_name='responsible')

    place = models.CharField('Local',max_length=100)

    description = models.TextField('Descrição',max_length=2000)

    user_hasCreated = models.ForeignKey('Accounts.CustomUser_DBTable',on_delete=models.CASCADE,related_name='user_hasCreated')

    questionKey = models.CharField('Chave da pergunta',max_length=100,null=True)
    status_choices = (
            ('Nova','Nova'),
            ('Em andamento','Em andamento'),
            ('Concluida','Concluida'),
            ('Cancelada','Cancelada'),
             )   
    status = models.CharField('Status',max_length=100,choices=status_choices,default='Nova')
    
    def __str__(self):
        return self.title

class Comment_DBTable (models.Model):
    user = models.ForeignKey('Accounts.CustomUser_DBTable',on_delete=models.CASCADE)
    comment = models.TextField('Comentário',max_length=2000)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='Ativo ou Elemento')
    # O campo object_id armazena o ID do objeto relacionado
    object_id = models.PositiveIntegerField(verbose_name='ID do Ativo/Elemento?')
    Instance = GenericForeignKey('content_type', 'object_id')
    questionKey = models.CharField('Chave da pergunta',max_length=100,null=True)


    def __str__(self):
        return self.comment





    
    