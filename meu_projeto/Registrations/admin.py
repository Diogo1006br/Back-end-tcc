from django.contrib import admin

# Register your models here.

from .models import Asset_DBTable,SubItem_DBTable,Asset_Sub_Element_DBTable,images,Action_DBTable,Comment_DBTable

class AssetAdmin(admin.ModelAdmin):
    list_display = ('assetName', 'form', 'is_ocult', 'project', 'status')
    search_fields = ('assetName', 'form', 'project', 'status')
    filter_horizontal = ('show_to',)

admin.site.register(Asset_DBTable, AssetAdmin)
class SubItemAdmin(admin.ModelAdmin):
    list_display = ('elementName', 'asset', 'form', 'is_ocult')
    search_fields = ('elementName', 'asset', 'form')
    filter_horizontal = ('show_to',)

admin.site.register(SubItem_DBTable, SubItemAdmin)

admin.site.register(Asset_Sub_Element_DBTable)
admin.site.register(images)
admin.site.register(Action_DBTable)
admin.site.register(Comment_DBTable)