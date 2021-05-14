from django.contrib import admin
from django.urls import path
from . import views

app_name = "medicine"

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('add_medicine/', views.add_medicine, name="add_medicine"),
    path('view_medicine/<int:id>', views.view_medicine, name="view_medicine"),
    path('profile/', views.profile, name="profile"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('send/', views.send_notification)
]
