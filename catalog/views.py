from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version


class ProductListView(ListView):
    model = Product


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        current_version = product.version_set.filter(current_version_indicator=True).first()
        if current_version:
            context['current_version'] = current_version
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.user or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для выполнения этого действия.")
        return redirect('catalog:home')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormSet = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormSet(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormSet(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.user

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для выполнения этого действия.")
        return redirect('catalog:home')


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