from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'activity_data', views.ActivityDataViewSet)

urlpatterns = [
    path('upload', views.EmissionCalculatorAPIView.as_view())
] + router.urls
