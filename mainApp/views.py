import time

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render
from django.template.context_processors import csrf


def index(request):
    return render(request, 'mainApp/homePage.html')


def contact(request):
    return render(request, 'mainApp/basic.html', {'values': ['If you have any question please contact us',
                                                             '060119977', 'mail@email.com']})


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
