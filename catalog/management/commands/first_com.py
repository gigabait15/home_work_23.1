import json
from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from catalog.models import Category, Product
from django.conf import settings
import os

class Command(BaseCommand):
    """
    Кастомная команда для наполнения БД из фикстур
    """

    def load_fixture(self, filename):
        file_path = os.path.join(settings.BASE_DIR, 'fixtures', filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def handle(self, *args, **options):
        """Удаление всех продуктов, категорий, пользователей, групп и прав"""
        Product.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()
        Group.objects.all().delete()
        Permission.objects.all().delete()

        """Создание списков для хранения"""
        product_for_create = []
        category_for_create = []

        # Получение данных из фикстур
        categories_data = self.load_fixture('fixtures/categories.json')
        products_data = self.load_fixture('fixtures/products.json')
        permissions_data = self.load_fixture('fixtures/permissions.json')
        groups_data = self.load_fixture('fixtures/groups.json')
        users_data = self.load_fixture('fixtures/users.json')

        # Создание категорий
        for category_data in categories_data:
            category_fields = category_data['fields']
            category_for_create.append(
                Category(name=category_fields['name'], description=category_fields['description'])
            )
        Category.objects.bulk_create(category_for_create)

        # Создание продуктов
        for product_data in products_data:
            product_fields = product_data['fields']
            category = Category.objects.get(pk=product_fields['category'])
            product_for_create.append(
                Product(name=product_fields['name'], category=category, other_fields=product_fields['other_fields'])
            )
        Product.objects.bulk_create(product_for_create)

        # Создание прав
        for permission_data in permissions_data:
            permission_fields = permission_data['fields']
            Permission.objects.update_or_create(
                pk=permission_data['pk'],
                defaults=permission_fields
            )

        # Создание групп и добавление прав
        for group_data in groups_data:
            group_fields = group_data['fields']
            group, created = Group.objects.update_or_create(
                pk=group_data['pk'],
                defaults={'name': group_fields['name']}
            )
            if created:
                permissions = Permission.objects.filter(pk__in=group_fields['permissions'])
                group.permissions.set(permissions)

        # Создание пользователей и добавление их в группы
        for user_data in users_data:
            user_fields = user_data['fields']
            user, created = User.objects.update_or_create(
                pk=user_data['pk'],
                defaults={
                    'email': user_fields['email'],
                    'is_staff': user_fields['is_staff'],
                    'is_superuser': user_fields['is_superuser'],
                    'is_active': user_fields['is_active'],
                }
            )
            if created:
                user.set_password(user_fields['password'])
                user.save()

                # Добавление пользователя в группы
                if 'groups' in user_fields:
                    groups = Group.objects.filter(pk__in=user_fields['groups'])
                    user.groups.set(groups)

        self.stdout.write(self.style.SUCCESS('Команда успешно выполнена'))
