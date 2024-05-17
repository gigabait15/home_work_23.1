from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    def __str__(self):
        return f'{self.name} {self.description} '

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    image = models.ImageField(upload_to='product/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(default=0, verbose_name='Цена за покупку')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')

    is_published = models.BooleanField(default=False, verbose_name='признак публикации')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'{self.name} {self.category} {self.created_at}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

class Version(models.Model):
    name = models.CharField(max_length=100, verbose_name='название версии')
    number_version = models.IntegerField(default=1, verbose_name='номер версии,')
    current_version_indicator = models.BooleanField(default=True, verbose_name='признак текущей версии')

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
