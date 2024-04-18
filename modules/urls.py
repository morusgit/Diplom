from django.urls import path

from modules.apps import ModulesConfig
from modules.views import ModuleCreateAPIView, ModuleListAPIView

app_name = ModulesConfig.name

urlpatterns = [
    path('create/', ModuleCreateAPIView.as_view(), name='module_create'),
    path('list/', ModuleListAPIView.as_view(), name='module_list'),
]
