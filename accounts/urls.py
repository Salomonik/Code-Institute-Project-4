from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'  # adding namespace for URLs

urlpatterns = [
    # Login and logout views
    path('login/', views.login_view, name='login'),  # Custom view for handling AJAX
    path('logout/', views.logout_view, name='logout'),  # Custom view for handling AJAX
    path('register/', views.register_view, name='register'),  # Custom view for handling AJAX
    path('profile/', views.profile, name='profile'),

    # Password reset paths
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',  # Updated to correct template path
             success_url='/accounts/password_reset/done/'
         ), 
         name='password_reset'),
    
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'  # Updated to correct template path
         ), 
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',  # Updated to correct template path
             success_url='/accounts/reset/done/'
         ), 
         name='password_reset_confirm'),
    
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'  # Updated to correct template path
         ), 
         name='password_reset_complete'),

    # Password change paths
    path('password_change/', 
         auth_views.PasswordChangeView.as_view(
             template_name='accounts/password_change.html',  # Custom template for password change
             success_url='/accounts/password_change/done/'
         ), 
         name='password_change'),
    
    path('password_change/done/', 
         auth_views.PasswordChangeDoneView.as_view(
             template_name='accounts/password_change_done.html'  # Custom template for password change confirmation
         ), 
         name='password_change_done'),
]
