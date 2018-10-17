from django.urls import path
from . import  views
# Create your url patterns

app_name = "grading_system"

urlpatterns = [
    path('test/', views.test, name='test'),
]
