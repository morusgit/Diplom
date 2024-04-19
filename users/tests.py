from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User

from unittest.mock import patch

from users.serializers import UserSerializer
from users.tasks import send_mail_confirmation, send_mail_notification, send_mail_notification_user_not_active


class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')

    def test_create_user(self):
        url = '/users/'
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.last().email, 'newuser@example.com')

    def test_get_user(self):
        new_user = User.objects.create_user(email='newuser@example.com', password='newpassword123')

        self.client.force_authenticate(user=new_user)

        url = f'/users/{new_user.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'newuser@example.com')

    def test_update_user(self):
        new_user = User.objects.create_user(email='newuser@example.com', password='newpassword123')

        self.client.force_authenticate(user=new_user)

        url = f'/users/{new_user.id}/'
        data = {
            'email': 'newnewuser@example.com',
            'password': 'newnewpassword123'
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'newnewuser@example.com')

    def test_delete_user(self):
        new_user = User.objects.create_user(email='newuser@example.com', password='newpassword123')

        self.client.force_authenticate(user=new_user)

        url = f'/users/{new_user.id}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TasksTestCase(TestCase):
    @patch('users.tasks.send_mail')
    def test_send_mail_confirmation(self, mock_send_mail):
        send_mail_confirmation('test@example.com', '12345')
        mock_send_mail.assert_called_once()

    @patch('users.tasks.send_mail')
    def test_send_mail_notification(self, mock_send_mail):
        send_mail_notification('test@example.com')
        mock_send_mail.assert_called_once()

    @patch('users.tasks.send_mail')
    def test_send_mail_notification_user_not_active(self, mock_send_mail):
        send_mail_notification_user_not_active('test@example.com')
        mock_send_mail.assert_called_once()


class UserSerializerTestCase(TestCase):
    def test_create_user(self):
        data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'telegram': 'test_telegram',
            'password': 'testpassword',
            'role': 'member',
            'is_active': True
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.telegram, 'test_telegram')
        self.assertTrue(user.check_password('testpassword'))
        self.assertEqual(user.role, 'member')
        self.assertTrue(user.is_active)
