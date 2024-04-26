from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mail/<str:pk>/', views.mail, name='mail'),
]