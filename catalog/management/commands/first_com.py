from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    """
    кастомная команда для наполнения бд
    """

    @staticmethod
    def json_read_categories():
        """Здесь мы получаем данные из фикстурв с категориями"""

        categories = Category.objects.all()
        return categories


    @staticmethod
    def json_read_products():
        """Здесь мы получаем данные из фикстурв с продуктами"""

        products = Product.objects.all()
        return products


    def handle(self, *args, **options):
        """Удаление всех продуктов и категорий"""
        Product.objects.all().delete()
        Category.objects.all().delete()

        """Создание списков для хранения"""
        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for category in self.json_read_categories():
            category_for_create.append(
                Category(name=category.name, description=category.description)
            )
        Category.objects.bulk_create(category_for_create)

            # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for product in self.json_read_products():
            # Получаем соответствующую категорию
            category = Category.objects.get(name=product.category.name)
            product_for_create.append(
                Product(name=product.name, category=category, other_fields=product.other_fields)
            )
        Product.objects.bulk_create(product_for_create)

        self.stdout.write(self.style.SUCCESS('Команда успешно выполнена'))
