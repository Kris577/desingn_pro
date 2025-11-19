from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('applications/create/', views.ApplicationCreate.as_view(), name='create_applications'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('applications/delete/<int:pk>/', views.ApplicationDelete.as_view(), name='delete_application'),
    path('admin-panel/', views.AdminPanel.as_view(), name='admin_panel'),

    path('change-status/', views.change_application_status, name='change_application_status'),
    path('add-category/', views.add_category, name='add_category'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),

]