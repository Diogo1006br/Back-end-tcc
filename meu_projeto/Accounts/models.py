from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractUser
from django.contrib.auth.models import Group, Permission
import datetime

class Base(models.Model):
    created = models.DateField('Criação', auto_now_add=True, null=True)
    modified = models.DateField('Modificação', auto_now=True, null=True)
    active = models.BooleanField("Ativo?", default=True, null=True)

    class Meta:
        abstract = True

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, companyId, password, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        user.companyId = companyId
        return user

    def create_user(self, email, companyId, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        company_instance = Company_DBTable.objects.get(id=companyId)
        return self._create_user(email, company_instance, password, **extra_fields)

    def create_superuser(self, email, companyId, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if not extra_fields.get('is_superuser') or not extra_fields.get('is_staff'):
            raise ValueError('Superuser precisa ter is_superuser e is_staff como True')

        company_instance = Company_DBTable.objects.get(id=companyId)
        return self._create_user(email=email, companyId=company_instance, password=password, **extra_fields)

class CustomUser_DBTable(AbstractUser, PermissionsMixin):
    email = models.EmailField('email', unique=True)
    firstName = models.CharField('Nome', max_length=100, null=True)
    lastName = models.CharField('Sobrenome', max_length=100, null=True)
    profileImage = models.ImageField('Imagem de Perfil', upload_to='usuarios/perfil', blank=True)
    companyPosition = models.CharField('Cargo', max_length=100, blank=True, null=True)
    birthDate = models.DateField('Data de Nascimento', null=True, blank=True)
    CPF = models.CharField('CPF', max_length=14, blank=True, null=True)
    phone = models.BigIntegerField('Telefone', blank=True, null=True)
    companyId = models.ForeignKey('Company_DBTable', null=True, on_delete=models.CASCADE)
    firstAcess = models.BooleanField('Primeiro Acesso?', default=True)
    registrationDate = models.DateField('Data de registro', default=datetime.datetime.now)
    lastConnection = models.DateField('Última conexão', null=True, default=datetime.datetime.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'companyId']

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name="customusuario_groups",
        related_query_name="customusuario",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name="customusuario_user_permissions",
        related_query_name="customusuario",
    )

    objects = UserManager()

    def __str__(self):
        return self.email

class Plans_DBTable(Base):
    planName = models.CharField('Nome do Plano', max_length=50, unique=True)
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    description = models.TextField('Descrição', blank=True)
    usersLimit = models.IntegerField('Limite de Usuários', blank=True)
    storageLimit = models.IntegerField('Limite de Armazenamento', blank=True)
    projectsLimit = models.IntegerField('Limite de Projetos', blank=True)

    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'

    def __str__(self):
        return self.planName

class Company_DBTable(Base):
    companyName = models.CharField('Nome da Empresa', max_length=50, unique=True)
    CNPJ = models.CharField('CNPJ', max_length=50)
    address = models.CharField('Endereço', max_length=100, blank=True, null=True)
    city = models.CharField('Cidade', max_length=50, blank=True, null=True)

    ESTADO_CHOICES = [
        ('Acre', 'Acre'), ('Alagoas', 'Alagoas'), ('Amapá', 'Amapá'),
        ('Amazonas', 'Amazonas'), ('Bahia', 'Bahia'), ('Ceará', 'Ceará'),
        ('Distrito Federal', 'Distrito Federal'), ('Espírito Santo', 'Espírito Santo'),
        ('Goiás', 'Goiás'), ('Maranhão', 'Maranhão'), ('Mato Grosso', 'Mato Grosso'),
        ('Mato Grosso do Sul', 'Mato Grosso do Sul'), ('Minas Gerais', 'Minas Gerais'),
        ('Pará', 'Pará'), ('Paraíba', 'Paraíba'), ('Paraná', 'Paraná'),
        ('Pernambuco', 'Pernambuco'), ('Piauí', 'Piauí'), ('Rio de Janeiro', 'Rio de Janeiro'),
        ('Rio Grande do Norte', 'Rio Grande do Norte'), ('Rio Grande do Sul', 'Rio Grande do Sul'),
        ('Rondônia', 'Rondônia'), ('Roraima', 'Roraima'), ('Santa Catarina', 'Santa Catarina'),
        ('São Paulo', 'São Paulo'), ('Sergipe', 'Sergipe'), ('Tocantins', 'Tocantins'),
    ]

    state = models.CharField('Estado', max_length=19, choices=ESTADO_CHOICES, blank=True, null=True)
    telephone = models.BigIntegerField('Telefone', blank=True, null=True)
    logotipo = models.ImageField('Logotipo', upload_to='empresas/logos', blank=True, null=True)
    users = models.ManyToManyField(CustomUser_DBTable, blank=True)
    plan = models.ForeignKey('Plans_DBTable', blank=True, on_delete=models.CASCADE, null=True)
    site = models.CharField('Site', blank=True, null=True)
    comercialEmail = models.EmailField('Email Comercial', blank=True, null=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

    def __str__(self):
        return self.companyName
