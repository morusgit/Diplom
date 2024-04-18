from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from modules.models import Module
from modules.paginators import ModulePagination
from modules.permissions import IsOwner, IsModerator, IsCustomAdmin
from modules.serializers import ModuleSerializer


# Create your views here.


class ModuleCreateAPIView(CreateAPIView):
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ModuleListAPIView(ListAPIView):
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    pagination_class = ModulePagination


class ModuleDetailAPIView(RetrieveAPIView):
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    permission_classes = [IsOwner | IsModerator | IsCustomAdmin]


class ModuleDestroyAPIView(DestroyAPIView):
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    permission_classes = [IsOwner | IsCustomAdmin]


class ModuleUpdateAPIView(UpdateAPIView):
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    permission_classes = [IsOwner | IsModerator | IsCustomAdmin]
