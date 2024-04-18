from celery import shared_task
from django.core.mail import send_mail

from config import settings


@shared_task
def send_mail_notification_module_changed(user_email, module_name):
    """Отправка письма с уведомлением об изменении модуля."""
    subject = 'Уведомление о изменении модуля на портале "Образовательные Модули".'
    message = f'Модуль "{module_name}" на который вы подписаны был изменен.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)
