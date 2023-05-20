from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('chats_data/', views.chats_data, name='chats_data'),
    path('send_request/<str:user>/', views.send_request, name='send_request'),
    path('request_action/<str:action>/', views.request_action, name='request_action'),
    path('get_convo/<str:friend>/', views.get_convo, name='get_convo'),
    path('send_message/', views.send_message, name='send_message'),
]
