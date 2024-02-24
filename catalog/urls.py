from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import home, contact, ProductListView, ProductDetailView, ProductCreateView

app_name = CatalogConfig.name


urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contact/', contact, name='contact'),
    path('view/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
]