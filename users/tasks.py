from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from users.models import User, UserRoles


@shared_task
def send_mail_confirmation(user_email, confirmation_code):
    """Отправка письма с кодом подтверждения."""
    url = f'{settings.SITE_URL}/users/confirm_registration/'
    subject = 'Подтверждение регистрации на портале "Образовательные Модули".'
    message = (f'Для подтверждения регистрации перейдите по ссылке:'
               f' {url} и используйте следующий код: {confirmation_code}')
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)


@shared_task
def send_mail_notification(user_email):
    """Отправка письма с уведомлением о регистрации."""
    subject = 'Уведомление о регистрации на портале "Образовательные Модули".'
    message = 'Вы успешно зарегистрировались на сайте.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)


def send_mail_notification_user_not_active(user_email):
    """Отправка письма с уведомлением о блокировке аккаунта."""
    subject = 'Уведомление о статусе аккаунта на портале "Образовательные Модули".'
    message = 'Ваш аккаунт заблокирован по причине долгого отсутствия активности.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)


@shared_task
def check_users_and_block_inactive():
    """Задача для проверки активности пользователей."""
    current_date = timezone.now().date()
    inactive_period = timezone.timedelta(days=30)
    inactive_date = current_date - inactive_period

    inactive_users = User.objects.filter(last_login__lt=inactive_date)
    for user in inactive_users:
        if user.role not in [UserRoles.ADMINISTRATOR, UserRoles.MODERATOR]:
            if user.is_active:
                send_mail_notification_user_not_active(user.email)
            user.is_active = False
            user.save()
