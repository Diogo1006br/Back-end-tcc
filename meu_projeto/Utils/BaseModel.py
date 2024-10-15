from django.db import models




class Base (models.Model):
    created_at = models.DateField('Criação', auto_now_add=True,null=True)
    uptaded_at= models.DateField('Modificação',auto_now=True,null=True)
    user_has_created = models.ForeignKey('Accounts.CustomUser_DBTable', on_delete=models.CASCADE, related_name='%(class)s_created',null=True)
    user_has_modified = models.ForeignKey('Accounts.CustomUser_DBTable', on_delete=models.CASCADE, related_name='%(class)s_modified',null=True)
    class Meta:
        abstract = True