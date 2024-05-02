from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name='home'),
    path('box/<str:name>/', views.box, name='box'),
    path('mail/<str:pk>/', views.mail, name='mail'),

    path('sendMail/', views.sendMail, name='sendMail'),
    path('respond/<str:pk>/', views.respond, name='respond'),
    path('moveMailToBox/<str:pk>/<str:name>/', views.moveMailToBox, name='moveMailToBox'),
    path('markUnreadOrRead/<str:pk>/', views.markUnreadOrRead, name='markUnreadOrRead'),
    path('deleteEmail/<str:pk>/', views.deleteEmail, name='deleteEmail'),
]