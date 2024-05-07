from django.urls import path
from . import views


urlpatterns = [
    # path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('/landing_page', views.landing_page, name='blog-home'),
    path('data_table/', views.data_table, name='data_table'),
]
