from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

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


class ProductUpdateView(UpdateView):
    model = Product
    fields = "__all__"

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:view', args=[self.kwargs.get('pk')])


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')


class ContactView(View):
    template_name = 'catalog/contact.html'

    def get(self, request):
        context = {'title': 'Контакты'}
        return render(request, self.template_name, context)

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('emails')
        message = request.POST.get('message')
        print(f'name:{name}\nemails:{email}\nmessage:{message}')

        context = {'title': 'Контакты'}
        return render(request, self.template_name, context)