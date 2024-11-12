from django.db import models

# Create your models here.
from email.policy import default
from django.db import models

# Create your models here.
import re

from django.db import models

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import  PermissionsMixin, BaseUserManager,AbstractUser

import datetime
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

class Base(models.Model):
    created = models.DateField('Criação', auto_now_add=True,null=True)
    modified = models.DateField('Modificação',auto_now=True,null=True)
    active = models.BooleanField("Ativo?",default=True,null=True)

    class Meta:
        abstract = True



#model do gerenciador de usuarios
class UserManager(BaseUserManager):
    use_in_migrations = True
    #define parametros de registro
    def _create_user(self, email,companyId, password, **extra_fields):
        #define email obrigatorio
        if not email:
            raise ValueError('o email é obrigatorio')
        #define padrão de email para evitar escrita erronea    
        email = self.normalize_email(email)
        #define os campos colocando email equivalente a username sendo usado para login agora     
        user = self.model(email = email, username=email,**extra_fields)  
        user.set_password(password)
        user.save(using=self._db)
        user.companyId = companyId
        return user
    #define a função de criação e istanciamento de usuario retornando o _create_user
    def create_user(self, email,companyId, password=None, **extra_fields ):
        #define o usuario como superuser false
        extra_fields.setdefault('is_superuser',False)
        company_instance = Company_DBTable.objects.get(id = companyId)
        return self._create_user(email, company_instance, password, **extra_fields)
    #define a função de criação e istanciamento de super usuario retornando o _create_user
    def create_superuser(self, email, companyId, password, **extra_fields):
            extra_fields.setdefault('is_superuser',True)
            extra_fields.setdefault('is_staff',True)
            
            if extra_fields.get('is_superuser') is not True:
                raise ValueError('superuser precisa ter is_superuser como True')

            if extra_fields.get('is_staff') is not True:
                raise ValueError('superuser precisa ter is_staff como True')
            
            company_instance = Company_DBTable.objects.get(id = companyId)
            
            return self._create_user(email=email,companyId=company_instance,password=password,**extra_fields)

#define os campos de registro de usuario
class CustomUser_DBTable(AbstractUser,PermissionsMixin):
    """
    Model representing a custom user.

    Attributes
    ----------
    **email : models.EmailField**
        The user's email. It's unique and used as the username field.

    **firstName : models.CharField**
        The user's first name.

    **lastName : models.CharField**
        The user's last name.

    **profileImage : models.ImageField**
        The user's profile image.

    **CompanyPosition : models.CharField**
        The user's position in the company.

    **birthDate : models.DateField**
        The user's birth date.

    **CPF : models.CharField**
        The user's CPF (Brazilian individual taxpayer registry identification).

    **telephone : models.BigIntegerField**
        The user's telephone number.

    **companyId : models.ForeignKey**
        Reference to the company the user belongs to.

    **groups : models.ManyToManyField**
        Groups the user belongs to. A user will get all permissions granted to each of their groups.

    **user_permissions : models.ManyToManyField**
        Specific permissions for this user.
    """
    email = models.EmailField('email', unique=True)
    #TODO: Definir as categorias de acesso para versão final
    #define as escolas do drop - Categorias de usuarios para definir acesso

    firstName = models.CharField('Nome',max_length=100,null=True)
    lastName = models.CharField('Sobrenome',max_length=100,null=True)

    profileImage = models.ImageField('Imagem de Perfil',upload_to = 'usuarios/perfil',blank=True)

    companyPosition = models.CharField('Cargo',max_length=100,blank=True,null=True)
    
    birthDate = models.DateField('Data de Nascimento',null=True,blank=True)

    CPF = models.CharField('CPF',max_length=14,blank=True,null=True)

    phone = models.BigIntegerField('Telefone',blank=True,null=True)

    companyId = models.ForeignKey('Company_DBTable',null=True, on_delete=models.CASCADE)
   
    firstAcess = models.BooleanField('Primeiro Acesso?',default=True)

    registrationDate = models.DateField('Data de registro', default=datetime.datetime.now)

    lastConnection = models.DateField('Ultima conexao', null=True, default=datetime.datetime.now)
    #define que o email fará o papel de username no form
    USERNAME_FIELD =  'email'
    #define os campos obrigatorios, outros campos não adicionados pois o django já os padroniza obrigatorios
    REQUIRED_FIELDS =  ['firstName','companyId']

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="customusuario_groups",
        related_query_name="customusuario",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customusuario_user_permissions",
        related_query_name="customusuario",
    )

    

    objects = UserManager()
    def __str__(self):
        return self.email

class Plans_DBTable(Base):
    """
    Model representing a plan.

    Attributes
    ----------
    **plan_name : models.CharField**
        The name of the plan. It's unique and has a maximum length of 50 characters.

    **price : models.DecimalField**
        The price of the plan.

    **description : models.TextField**
        A detailed description of the plan. This field can be left blank.

    **users_limit : models.IntegerField**
        The limit of users for the plan. This field can be left blank.

    **storage_limit : models.IntegerField**
        The storage limit for the plan. This field can be left blank.

    **projects_limit : models.IntegerField**
        The limit of projects for the plan. This field can be left blank.
    """
    planName = models.CharField('Nome do Plano',max_length=50,unique=True)
    price = models.DecimalField('Preço',max_digits=10,decimal_places=2)
    description = models.TextField('Descrição',blank=True)
    usersLimit = models.IntegerField('Limite de Usuários',blank=True)
    storageLimit = models.IntegerField('Limite de Armazenamento',blank=True)
    projectsLimit = models.IntegerField('Limite de Projetos',blank=True)

    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'
    
    def __str__(self):
        return self.plan_name

class Company_DBTable(Base):
    """
    Model representing a company.

    Attributes
    ----------
    **company_name : models.CharField**
        The name of the company. It's unique and has a maximum length of 50 characters.

    **CNPJ : models.CharField**
        The CNPJ of the company. CNPJ is the Brazilian company identification number.

    **address : models.CharField**
        The address of the company. This field can be left blank.

    **city : models.CharField**
        The city where the company is located. This field can be left blank.

    **state : models.CharField**
        The state where the company is located. This field can be left blank.

    **telephone : models.BigIntegerField**
        The telephone number of the company. This field can be left blank.

    **logotipo : models.ImageField**
        The logo of the company. This field can be left blank.

    **users : models.ManyToManyField**
        The users associated with the company. This field can be left blank.

    **plan : models.ForeignKey**
        The plan associated with the company. This field can be left blank.

    **site : models.URLField**
        The website of the company. This field can be left blank.

    **comercial_email : models.EmailField**
        The commercial email of the company. This field can be left blank.
    """
    companyName = models.CharField('Nome da Empresa',max_length=50,unique=True)
    CNPJ = models.CharField('CNPJ',max_length=50)
    address = models.CharField('Endereço',max_length=100,blank=True, null=True)
    city = models.CharField('Cidade',max_length=50,blank=True, null=True)
    
    ESTADO_CHOICES = (
        ('Acre','Acre'),
        ('Alagoas','Alagoas'),
        ('Amapá','Amapá'),
        ('Amazonas','Amazonas'),
        ('Bahia','Bahia'),
        ('Ceará','Ceará'),
        ('Distrito Federal','Distrito Federal'),
        ('Espírito Santo','Espírito Santo'),
        ('Goiás','Goiás'),
        ('Maranhão','Maranhão'),
        ('Mato Grosso','Mato Grosso'),
        ('Mato Grosso do Sul','Mato Grosso do Sul'),
        ('Minas Gerais','Minas Gerais'),
        ('Pará','Pará'),
        ('Paraíba','Paraíba'),
        ('Paraná','Paraná'),
        ('Pernambuco','Pernambuco'),
        ('Piauí','Piauí'),
        ('Rio de Janeiro','Rio de Janeiro'),
        ('Rio Grande do Norte','Rio Grande do Norte'),
        ('Rio Grande do Sul','Rio Grande do Sul'),
        ('Rondônia','Rondônia'),
        ('Roraima','Roraima'),
        ('Santa Catarina','Santa Catarina'),
        ('São Paulo','São Paulo'),
        ('Sergipe','Sergipe'),
        ('Tocantins','Tocantins'),)
    state = models.CharField('Estado',max_length=19,choices=ESTADO_CHOICES,blank=True, null=True)

    telephone = models.BigIntegerField('Telefone',blank=True, null=True)

    logotipo = models.ImageField('Logotipo',upload_to = 'empresas/logos',blank=True, null=True)

    users = models.ManyToManyField(CustomUser_DBTable,blank=True,null=True)
    plan = models.ForeignKey('Plans_DBTable',blank=True, on_delete=models.CASCADE,null=True)

    site = models.CharField('Site',blank=True,null=True)
    comercialEmail = models.EmailField('Email Comercial',blank=True,null=True)


    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
    
    def __str__(self):
        return self.companyName
    


    
