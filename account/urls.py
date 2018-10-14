from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('change/password/', views.change_password, name='change_password'),
]
