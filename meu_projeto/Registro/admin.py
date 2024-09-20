from django.contrib import admin

# Register your models here.

from .models import Asset_DBTable,SubItem_DBTable,Asset_Sub_Element_DBTable,images,Action_DBTable,Comment_DBTable

admin.site.register(Asset_DBTable)
admin.site.register(SubItem_DBTable)
admin.site.register(Asset_Sub_Element_DBTable)
admin.site.register(images)
admin.site.register(Action_DBTable)
admin.site.register(Comment_DBTable)