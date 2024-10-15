from django.db import models
from Utils.BaseModel import Base

# Create your models here.

class Project_DBTable(Base):
    """
    Model representing a project.

    Attributes
    ----------
    **project_name : models.CharField**
        The project name (max of 100 chars).

    **project_description : models.TextField**
        A detailed description of the project.

    **participants : models.ManyToMany**
        The participants of the project.

    **image : models.ImageField**
        The image of the project.

    **owner : models.ForeignKey**
        The owner of the project.
    """
    projectName = models.CharField(max_length=100)
    projectDescription = models.TextField()
    members = models.ManyToManyField('Accounts.CustomUser_DBTable')
    image = models.ImageField(upload_to='projects_images/', default='projects_images/default.jpg')
    owner = models.ForeignKey('Accounts.Company_DBTable', on_delete=models.CASCADE)

    choices = (
        ('Arquivado','Arquivado'),
        ('Ativo','Ativo'),
    )
    status = models.CharField('Status',max_length=100,choices=choices,default='Ativo')

    def __str__(self):
        return self.projectName