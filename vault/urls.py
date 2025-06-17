from django.urls import path
from . import views

urlpatterns = [
    path('', views.password_list, name='password_list'),
    path('add/', views.password_create, name='password_create'),
    path('<int:pk>/', views.password_detail, name='password_detail'),
    path('<int:pk>/edit/', views.password_edit, name='password_edit'),
    path('<int:pk>/delete/', views.password_delete, name='password_delete'),
    path('generate-password/', views.generate_password, name='generate_password'),
    path('wallets/', views.wallet_list, name='wallet_list'),
    path('wallets/add/', views.wallet_create, name='wallet_create'),
    path('wallets/<int:pk>/', views.wallet_detail, name='wallet_detail'),
    path('wallets/<int:pk>/edit/', views.wallet_edit, name='wallet_edit'),
    path('wallets/<int:pk>/delete/', views.wallet_delete, name='wallet_delete'),
    path('notes/', views.note_list, name='note_list'),
    path('notes/add/', views.note_create, name='note_create'),
    path('notes/<int:pk>/', views.note_detail, name='note_detail'),
    path('notes/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('notes/<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('save-events/', views.save_event_list, name='save_event_list'),
    path('save-events/add/', views.save_event_create, name='save_event_create'),
    path('save-events/<int:pk>/', views.save_event_detail, name='save_event_detail'),
    path('save-events/<int:pk>/edit/', views.save_event_edit, name='save_event_edit'),
    path('save-events/<int:pk>/delete/', views.save_event_delete, name='save_event_delete'),
    path('password-generator/', views.password_generator, name='password_generator'),
]
