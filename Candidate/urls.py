from django.urls import path
from . import views

app_name = 'Candidate'
urlpatterns = [
    path('', views.home, name='home'),
    path('choicefilling/', views.ChoiceFilling, name="choicefilling"),
    path('user_login/', views.user_login, name='user_login'),
    path('change_password/', views.change_password, name='change_password'),
    path('register/', views.register, name='register'),

]
