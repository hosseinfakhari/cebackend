from django.urls import path
from . import views

urlpatterns = [
    path('', views.EmissionCalculatorAPIView.as_view())
]
