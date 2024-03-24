from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='place-home'),
    path('about/', views.about, name='place-about'),
]