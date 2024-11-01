from django.contrib import admin
from .models import CustomUser_DBTable, Plans_DBTable, Company_DBTable

@admin.register(CustomUser_DBTable)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'firstName', 'lastName', 'companyId')
    search_fields = ('email', 'firstName', 'lastName')
    filter_horizontal = ('groups', 'user_permissions')

@admin.register(Plans_DBTable)
class PlansAdmin(admin.ModelAdmin):
    list_display = ('planName', 'price', 'usersLimit', 'storageLimit', 'projectsLimit')
    search_fields = ('planName',)

@admin.register(Company_DBTable)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('companyName', 'CNPJ', 'address', 'city', 'state')
    search_fields = ('companyName', 'CNPJ')
    filter_horizontal = ('users',)