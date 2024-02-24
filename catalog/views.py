from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from catalog.models import Product


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'

class ProductCreateView(CreateView):
    model = Product
    fields = "__all__"
    success_url = reverse_lazy('catalog:home')


def home(request):
    return render(request, 'catalog/product_list.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} {email} {message}')

    context = {
        'title': 'Контакты'
    }
    return render(request, 'catalog/contact.html', context)