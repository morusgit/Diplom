from celery import shared_task
from django.core.mail import send_mail
from config import settings


@shared_task
def send_mail_confirmation(user_email, confirmation_code):
    subject = 'Подтверждение регистрации на портале "Образовательные Модули".'
    message = f'Для подтверждения регистрации используйте следующий код: {confirmation_code}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)


@shared_task
def send_mail_notification(user_email):
    subject = 'Уведомление о регистрации на портале "Образовательные Модули".'
    message = 'Вы успешно зарегистрировались на сайте.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)
