from django.contrib import admin
from modules.models import Module


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'name', 'description', 'url_video', 'last_update', 'owner', 'is_published')
    search_fields = ('serial_number', 'name', 'description', 'image', 'url_video', 'last_update', 'owner')
    list_filter = ('serial_number', 'name', 'description', 'image', 'url_video', 'last_update', 'owner')
