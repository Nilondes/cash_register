from django.urls import path
from .views import create_check

urlpatterns = [
    path('v1/cash_machine', create_check, name='create_check'),
]