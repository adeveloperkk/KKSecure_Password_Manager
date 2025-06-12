from django.urls import path
from . import views

urlpatterns = [
    path('', views.password_list, name='password_list'),
    path('add/', views.password_create, name='password_create'),
    path('<int:pk>/', views.password_detail, name='password_detail'),
    path('<int:pk>/edit/', views.password_edit, name='password_edit'),
    path('<int:pk>/delete/', views.password_delete, name='password_delete'),
    path('generate-password/', views.generate_password, name='generate_password'),
    path('import/', views.import_passwords, name='import_passwords'),
    path('export/', views.export_passwords, name='export_passwords'),
]
