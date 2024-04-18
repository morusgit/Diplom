import os

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from modules.models import Module, Subscription
from modules.serializers import ModuleSerializer, SubscriptionSerializer
from rest_framework import serializers
from modules.validators import ForbiddenWordsValidator, YoutubeUrlValidator
from users.models import User

from users.models import UserRoles
from rest_framework.exceptions import PermissionDenied
from unittest.mock import Mock
from modules.permissions import IsOwner, IsModerator, IsCustomAdmin

from django.test import override_settings

from django.test import TestCase
from modules.tasks import send_mail_notification_module_changed
from unittest.mock import patch


class ModuleTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@ya.ru',
            password='test12345',
        )
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_create_module(self):
        response = self.client.post(
            '/modules/create/', {
                'user': self.user.pk,
                'name': 'test',
                'description': 'test',
                'serial_number': 1
            }
        )
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Module.objects.count(), 1)
        self.assertEqual(Module.objects.get().name, 'test')
        self.assertEqual(response.json()['name'], 'test')

    def test_list_module(self):
        data = {
            'user': self.user.pk,
            'name': 'test',
            'description': 'test',
            'serial_number': 1
        }

        response = self.client.post('/modules/create/', data)
        print(response.json())

        response = self.client.get('/modules/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 4)

    def test_detail_module(self):
        data = {
            'user': self.user.pk,
            'name': 'test',
            'description': 'test',
            'serial_number': 1
        }

        response = self.client.post('/modules/create/', data)
        print(response.json())

        response = self.client.get('/modules/detail/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'test')

    def test_delete_module(self):
        data = {
            'user': self.user.pk,
            'name': 'test',
            'description': 'test',
            'serial_number': 1
        }

        response = self.client.post('/modules/create/', data)
        print(response.json())

        response = self.client.delete('/modules/delete/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_module(self):
        data = {
            'user': self.user.pk,
            'name': 'test',
            'description': 'test',
            'serial_number': 1
        }

        response = self.client.post('/modules/create/', data)
        print(response.json())

        data_update = {
            'user': self.user.pk,
            'name': 'test_update',
            'description': 'test_update',
            'serial_number': 1
        }

        response = self.client.put('/modules/update/1/', data_update)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'test_update')

    def test_like(self):
        data = {
            'user': self.user.pk,
            'name': 'test',
            'description': 'test',
            'serial_number': 1,
            'likes': 0
        }

        response = self.client.post('/modules/create/', data)
        print(response.json())

        response = self.client.post('/modules/like/1/')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_module_with_serial_number(self):
        response = self.client.post(
            '/modules/create/', {
                'user': self.user.pk,
                'name': 'test',
                'description': 'test',
                'serial_number': 1
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Module.objects.count(), 1)
        self.assertEqual(Module.objects.get().name, 'test')
        self.assertEqual(response.json()['name'], 'test')

        response = self.client.post(
            '/modules/create/', {
                'user': self.user.pk,
                'name': 'test2',
                'description': 'test2',
                'serial_number': 2
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Module.objects.count(), 2)
        self.assertEqual(Module.objects.last().name, 'test2')
        self.assertEqual(response.json()['name'], 'test2')

    def test_module_serializer_validators(self):
        module_data = {
            'name': 'Test Module',
            'description': 'This is a test module',
            'url_video': 'https://www.youtube.com/watch?v=12345'
        }
        context = {'request': self.client.request().wsgi_request}
        serializer = ModuleSerializer(data=module_data, context=context)
        self.assertTrue(serializer.is_valid())

    def test_module_serializer_invalidators(self):
        module_data = {
            'name': 'Test Module',
            'description': 'This is a test module',
            'url_video': 'invalid_url'
        }
        context = {'request': self.client.request().wsgi_request}
        serializer = ModuleSerializer(data=module_data, context=context)
        self.assertFalse(serializer.is_valid())


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@example.com', password='password1')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password2')
        self.module = Module.objects.create(name='Test Module', description='Test Description', owner=self.user1)

    def test_subscription_creation(self):
        subscription = Subscription.objects.create(user=self.user2, module=self.module)
        print(subscription)
        self.assertEqual(subscription.user, self.user2)
        self.assertEqual(subscription.module, self.module)

    def test_subscription_str_method(self):
        subscription = Subscription.objects.create(user=self.user2, module=self.module)
        self.assertEqual(str(subscription), f'{self.user2} - {self.module}')

    def test_subscription_unique_together_constraint(self):
        with self.assertRaises(Exception):
            Subscription.objects.create(user=self.user2, module=self.module)
            Subscription.objects.create(user=self.user2, module=self.module)


class PermissionsTestCase(APITestCase):
    def setUp(self):
        self.user = Mock()
        self.view = Mock()

    def test_is_owner_permission(self):
        permission = IsOwner()
        obj = Mock(owner=self.user)

        request = Mock(user=self.user)

        self.assertTrue(permission.has_object_permission(request, self.view, obj))

        other_user = Mock()
        request.user = other_user
        self.assertFalse(permission.has_object_permission(request, self.view, obj))

    def test_is_moderator_permission(self):
        permission = IsModerator()

        moderator_user = Mock(is_authenticated=True, role=UserRoles.MODERATOR)
        request_moderator = Mock(user=moderator_user)

        self.assertTrue(permission.has_permission(request_moderator, self.view))

        regular_user = Mock(is_authenticated=True, role=UserRoles.MEMBER)
        request_regular_user = Mock(user=regular_user)

        self.assertFalse(permission.has_permission(request_regular_user, self.view))

        request_not_authenticated = Mock(user=Mock(is_authenticated=False))
        with self.assertRaises(PermissionDenied):
            permission.has_permission(request_not_authenticated, self.view)

    def test_is_custom_admin_permission(self):
        permission = IsCustomAdmin()

        admin_user = Mock(is_authenticated=True, role=UserRoles.ADMINISTRATOR)
        request_admin = Mock(user=admin_user)

        self.assertTrue(permission.has_permission(request_admin, self.view))

        moderator_user = Mock(is_authenticated=True, role=UserRoles.MODERATOR)
        request_moderator = Mock(user=moderator_user)

        self.assertFalse(permission.has_permission(request_moderator, self.view))

        request_not_authenticated = Mock(user=Mock(is_authenticated=False))
        with self.assertRaises(PermissionDenied):
            permission.has_permission(request_not_authenticated, self.view)


class SendMailNotificationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@ya.ru',
            password='test12345',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_send_mail_notification_module_changed(self):
        user_email = 'test@example.com'
        module_name = 'Test Module'
        test_email = os.getenv('EMAIL_HOST_USER')

        with patch('modules.tasks.send_mail') as mock_send_mail:
            send_mail_notification_module_changed(user_email, module_name)

            mock_send_mail.assert_called_once_with(
                'Уведомление о изменении модуля на портале "Образовательные Модули".',
                f'Модуль "{module_name}" на который вы подписаны был изменен.',
                test_email,
                [user_email],
            )

        self.assertEqual(mock_send_mail.call_count, 1)


class ValidatorsTestCase(TestCase):
    def test_forbidden_words_validator(self):
        forbidden_words_validator = ForbiddenWordsValidator(field='content')

        with self.assertRaises(serializers.ValidationError) as context:
            forbidden_words_validator({'content': 'This message contains the word дурак'})
        self.assertIn('Недопустимые слова в content', str(context.exception))

        try:
            forbidden_words_validator({'content': 'This message is clean'})
        except serializers.ValidationError:
            self.fail('forbidden_words_validator raised ValidationError unexpectedly!')

    def test_youtube_url_validator(self):
        youtube_url_validator = YoutubeUrlValidator(field='video_url')

        with self.assertRaises(serializers.ValidationError) as context:
            youtube_url_validator({'video_url': 'https://www.invalidurl.com'})

        self.assertIn('Недопустимая ссылка на видео', str(context.exception))

        try:
            youtube_url_validator({'video_url': 'https://www.youtube.com/watch?v=validvideoid'})
        except serializers.ValidationError:
            self.fail('youtube_url_validator raised ValidationError unexpectedly!')
