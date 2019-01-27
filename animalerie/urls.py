from django.urls import path

from .import views

app_name= 'animalerie'

urlpatterns = [
    path('', views.index, name='index'),
    path('action/', views.action, name='action'),
    path('action/refresh/', views.index, name='refresh')
]