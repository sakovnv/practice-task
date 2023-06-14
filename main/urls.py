from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register', views.Register.as_view(), name='register'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.user_logout, name='logout'),
    path('profile', views.Profile.as_view(), name='profile'),

]