from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from modules.models import Module, Subscription
from modules.paginators import ModulePagination
from modules.permissions import IsOwner, IsModerator, IsCustomAdmin
from modules.serializers import ModuleSerializer, SubscriptionSerializer
from rest_framework.response import Response


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

    def get_object(self):
        """ Подсчет просмотров """
        data = super().get_object()
        data.views_count += 1
        data.save()
        return data


class ModuleDestroyAPIView(DestroyAPIView):
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    permission_classes = [IsOwner | IsCustomAdmin]


class ModuleUpdateAPIView(UpdateAPIView):
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    permission_classes = [IsOwner | IsModerator | IsCustomAdmin]


class SetLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, module_id):
        """ Поставить лайк """
        try:
            module = Module.objects.get(pk=module_id)
            user = request.user

            if user in module.liked_users.all():
                return Response(
                    {'error': 'Вы уже поставили лайк для этого модуля'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                module.likes += 1
                module.liked_users.add(user)
                module.save()
                return Response({'message': 'Лайк успешно поставлен'}, status=status.HTTP_200_OK)
        except Module.DoesNotExist:
            return Response({'error': 'Модуль не найден'}, status=status.HTTP_404_NOT_FOUND)


class SubscriptionView(APIView):
    def post(self, request, pk, *args, **kwargs):
        user = request.user
        module = get_object_or_404(Module, pk=pk)

        if module:
            subscription, created = Subscription.objects.get_or_create(user=user, module=module)
            if created:
                message = 'Подписка оформлена'
            else:
                subscription.delete()
                message = 'Подписка отменена'
            return Response({'message': message}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Модуль не найден'}, status=status.HTTP_404_NOT_FOUND)
