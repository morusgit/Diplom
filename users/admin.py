from django.contrib import admin
from users.models import User


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    """ Админка пользователей """
    list_display = ('email', 'first_name', 'last_name', 'telegram', 'is_active', 'role')
    search_fields = ('email', 'first_name', 'last_name', 'telegram')
    list_filter = ('email', 'first_name', 'last_name', 'telegram')
