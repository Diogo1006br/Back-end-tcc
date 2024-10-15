from django.contrib import admin
from django.utils.html import format_html
from .models import Form, FormResponse, DropboxAnswerList
class formsAdmin(admin.ModelAdmin):
    search_fields = ('name','form', 'company')

    list_display = ('id','name','form', 'company', 'created_at', 'updated_at')

  # Import the Form class

admin.site.register(Form, formsAdmin)

class formResponseAdmin(admin.ModelAdmin):
    search_fields = ('form_id','response', 'content_type', 'object_id', 'Instance')

    list_display = ('id','formID','response', 'content_type', 'object_id', 'Instance', 'created_at', 'updated_at')

  # Import the FormResponse class

admin.site.register(FormResponse, formResponseAdmin)


class DropboxAnswerListAdmin(admin.ModelAdmin):
    search_fields = ('id','list', 'company')

    list_display = ('id','list', 'company')

  # Import the DropboxAnswerList class

admin.site.register(DropboxAnswerList, DropboxAnswerListAdmin)