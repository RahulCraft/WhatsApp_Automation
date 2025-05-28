from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Auth & User Handling
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # Send WhatsApp Message (client side)
    path('send-message/', views.send_message, name='send_message'),
    path('message-sent-success/', views.index, name='message_sent_success'),  # Or a success template

    # Ajax-based login check
    path('check-login/', views.check_login, name='check_login'),
    path('ajax-login/', views.ajax_login, name='ajax_login')
]
