from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Project_DBTable

@admin.register(Project_DBTable)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('projectName', 'owner')
    search_fields = ('projectName', 'owner__company_name')
    filter_horizontal = ('members',)