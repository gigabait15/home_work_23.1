from django.shortcuts import render


def home(request):
    return render(request, 'catalog/home.html')

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