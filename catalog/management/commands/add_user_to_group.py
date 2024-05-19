from django.core.management import BaseCommand
from django.contrib.auth.models import Group
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user_email = "moder@sky.pro"
        user = User.objects.get(email=user_email)
        moderators_group = Group.objects.get(name="moderators")
        user.groups.add(moderators_group)

        print(f"Пользователь с email {user.email} добавлен в группу 'Модераторы'.")
