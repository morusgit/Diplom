from django.urls import path

from modules.apps import ModulesConfig
from modules.views import ModuleCreateAPIView, ModuleListAPIView, ModuleDetailAPIView, ModuleDestroyAPIView, \
    ModuleUpdateAPIView, SetLikeAPIView, SubscriptionView

app_name = ModulesConfig.name

urlpatterns = [
    path('create/', ModuleCreateAPIView.as_view(), name='module_create'),
    path('list/', ModuleListAPIView.as_view(), name='module_list'),
    path('detail/<int:pk>/', ModuleDetailAPIView.as_view(), name='module_detail'),
    path('delete/<int:pk>/', ModuleDestroyAPIView.as_view(), name='module_delete'),
    path('update/<int:pk>/', ModuleUpdateAPIView.as_view(), name='module_update'),
    path('like/<int:module_id>/', SetLikeAPIView.as_view(), name='module_like'),
    path('subscription/<int:pk>/', SubscriptionView.as_view(), name='module_subscription'),
]
