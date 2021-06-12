from django.core.files.storage import FileSystemStorage
from django.shortcuts import render


def index(request):
    return render(request, 'mainApp/homePage.html')



def upload_image(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['target'] = fs.url(name)
        context['generated'] = fs.url(name)
    return render(request, 'mainApp/homePage.html', context)


def ga(request):
    return render(request, 'mainApp/homePage.html')


def pso(request):
    return render(request, 'mainApp/homePage.html')


def gan(request):
    return render(request, 'mainApp/homePage.html')


def can(request):
    return render(request, 'mainApp/homePage.html')
