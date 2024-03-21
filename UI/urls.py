from django.urls import path
from . import views

urlpatterns = [
    path('UI/', views.members, name='members'),
]
