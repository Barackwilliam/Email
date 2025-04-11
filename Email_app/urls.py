from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('send-selected/', views.send_selected_emails, name='send_selected'),
    path('send-all/', views.send_to_all_emails, name='send_all'),
    path('all-emails/', views.all_emails, name='all_emails'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('add_email/', views.add_email, name='add_email'),
    path('compose/', views.send_custom_message, name='send_custom_message'),
    path('compose/', views.send_custom_message, name='compose_message'),
    path('all-emails-by-user/', views.all_emails_by_user, name='all_emails_by_user'),



]
