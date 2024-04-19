import random
import string

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.permissions import IsOwner, IsModerator
from users.serializers import UserSerializer
from users.tasks import send_mail_notification, send_mail_confirmation


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """ Просмотр пользователей и регистрация новых пользователей """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """ Установка прав для действий """
        if self.action in ['create']:
            permission_classes = [AllowAny]

        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser | IsOwner]

        elif self.action in ['list']:
            permission_classes = [IsAdminUser | IsModerator]

        elif self.action in ['retrieve']:
            permission_classes = [IsAdminUser | IsOwner]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """ Регистрация нового пользователя и отправка кода подтверждения """
        user = serializer.save()
        confirmation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        user.confirmation_code = confirmation_code
        user.save()

        send_mail_confirmation.delay(user.email, confirmation_code)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegistrationConfirmationView(APIView):
    """ Подтверждение регистрации """
    def post(self, request):
        email = request.data.get('email')
        confirmation_code = request.data.get('confirmation_code')

        try:
            user = User.objects.get(email=email)
            if user.confirmation_code == confirmation_code:
                user.is_active = True
                user.save()
                send_mail_notification.delay(user.email)
                return Response({'message': 'Регистрация успешно подтверждена'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Неверный код подтверждения'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
