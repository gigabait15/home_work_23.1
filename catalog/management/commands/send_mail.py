from django.core.mail import send_mail
from django.core.management import BaseCommand

from config import settings


class Command(BaseCommand):

    def handle(self, *args, **options):
        from_email = settings.EMAIL_HOST_USER
        subject = 'Поздравляем'
        message = 'Ваша публикация набрала '
        recipient_email = settings.EMAIL_HOST_USER

        try:
            send_mail(subject, message, from_email, [recipient_email])
            print("Письмо успешно отправлено")
        except Exception as e:
            # Логирование ошибок отправки письма
            print(f'Ошибка отправки письма: {e}')

        return None