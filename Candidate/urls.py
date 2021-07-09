from django.urls import path
from . import views
app_name = 'Candidate'
urlpatterns = [
   path('', views.home, name='home'),
]