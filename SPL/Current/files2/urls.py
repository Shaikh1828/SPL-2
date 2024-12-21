# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),  # About page
    path('contact/', views.contact, name='contact'),  # Contact page
    path("check-device/", views.check_device, name="check_device"),
    path("list-packages/", views.list_packages, name="list_packages"),
    path("extract-apk/", views.extract_apk, name="extract_apk"),
    # path('result/', views.result_view, name='result_view'),    
]



