from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'  # dodajemy namespace dla URL-i

urlpatterns = [
    # Widoki logowania i wylogowania
    path('login/', views.login_view, name='login'),  # Własny widok do obsługi AJAX
    path('logout/', views.logout_view, name='logout'),  # Własny widok do obsługi AJAX
    path('register/', views.register_view, name='register'),  # Własny widok do obsługi AJAX
    path('profile/', views.profile, name='profile'),

    # Ścieżki do resetowania hasła
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             success_url='/accounts/password_reset/done/'
         ), 
         name='password_reset'),
    
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url='/accounts/reset/done/'
         ), 
         name='password_reset_confirm'),
    
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ), 
         name='password_reset_complete'),

    # Ścieżki do zmiany hasła
    path('password_change/', 
         auth_views.PasswordChangeView.as_view(
             template_name='accounts/password_change.html',
             success_url='/accounts/password_change/done/'
         ), 
         name='password_change'),
    
    path('password_change/done/', 
         auth_views.PasswordChangeDoneView.as_view(
             template_name='accounts/password_change.html'
         ), 
         name='password_change_done'),
]