from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('change/password/', views.change_password, name='change_password'),
    path('view/update/profile/', views.view_update_profile,
         name='view_update_profile'),
]
