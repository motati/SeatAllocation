from django.contrib import admin
from django.urls import path, include
from Candidate import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('candidate/', include('Candidate.urls', namespace="Candidate")),
    path('', views.home, name='home'),
    path('logout/', views.user_logout, name='logout'),
    path('assign/', views.assign, name='assign'),
    path('tozero/', views.brnull, name='tozero'),
    path('assign-admin/', views.admin_home, name='admin_home'),
    path('tofreeze/', views.to_freeze, name='tofreeze'),
    path('toslide/', views.to_slide, name='toslide'),
    path('toremove/', views.to_remove, name='toremove'),
]


