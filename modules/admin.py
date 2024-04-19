from django.contrib import admin
from modules.models import Module, Subscription


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """Админка модулей"""
    list_display = ('serial_number', 'name', 'description', 'url_video', 'last_update', 'owner', 'is_published')
    search_fields = ('serial_number', 'name', 'description', 'image', 'url_video', 'last_update', 'owner')
    list_filter = ('serial_number', 'name', 'description', 'image', 'url_video', 'last_update', 'owner')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Админка подписок"""
    list_display = ('user', 'module')
    search_fields = ('user', 'module')
    list_filter = ('user', 'module')
