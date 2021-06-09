from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^upload_image/$', views.upload_image, name='image'),
    url(r'^ga/$', views.ga, name='ga'),
    url(r'^pso/$', views.pso, name='pso'),
    url(r'^gan/$', views.gan, name='gan'),
    url(r'^can/$', views.can, name='can'),
    url(r'^cancel/$', views.index, name='index'),
]
