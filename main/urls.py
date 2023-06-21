from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register', views.Register.as_view(), name='register'),
    path('login', views.Login.as_view(), name='login'),
    path('logout', views.user_logout, name='logout'),
    path('profile', views.Profile.as_view(), name='profile'),
    path('computations', views.Computations.as_view(), name='computations'),
    path('computations/save_as_pdf', views.save_as_pdf, name='save_as_pdf'),
    path('computations/save_as_json', views.save_as_json, name='save_as_json'),
]