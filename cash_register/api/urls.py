from django.urls import path
from .views import CheckCreationView, CheckView

urlpatterns = [
    path('v1/cash_machine', CheckCreationView.as_view(), name='check_creation'),
    path('v1/media/<str:filename>', CheckView.as_view(), name='check_view'),
]