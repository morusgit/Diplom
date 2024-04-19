from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.

NULLABLE = {
    'null': True,
    'blank': True,
}


class UserRoles(models.TextChoices):
    """Роли пользователей."""
    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')
    ADMINISTRATOR = 'admin', _('admin')


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер для модели пользователя."""
    def create_user(self, email, password=None, **extra_fields):
        """Создает и сохраняет пользователя с имейлом."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создает и сохраняет пользователя супервайзера."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if extra_fields.get('role') is not UserRoles.ADMINISTRATOR:
            extra_fields['role'] = UserRoles.ADMINISTRATOR

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Модель пользователя."""
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    first_name = models.CharField(max_length=150, verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='фамилия', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='активирован')
    telegram = models.CharField(max_length=50, verbose_name='телеграм', **NULLABLE)
    confirmation_code = models.CharField(max_length=50, verbose_name='код подтверждения', **NULLABLE)
    role = models.CharField(max_length=25, choices=UserRoles.choices, default=UserRoles.MEMBER, verbose_name='роль')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('pk',)
