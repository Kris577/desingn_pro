from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('applications/create/', views.ApplicationCreate.as_view(), name='create_applications'),]