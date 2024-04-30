from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('box/<str:name>/', views.box, name='box'),
    path('mail/<str:pk>/', views.mail, name='mail'),

    path('sendMail/', views.sendMail, name='sendMail'),
    path('respond/<str:pk>/', views.respond, name='respond'),
    path('deleteEmail/<str:pk>/', views.deleteEmail, name='deleteEmail'),
]