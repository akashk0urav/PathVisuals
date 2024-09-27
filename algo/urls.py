from django.urls import path
from .views import find_path

urlpatterns = [
    path('', find_path, name='find_path'),
]
