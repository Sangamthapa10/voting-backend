from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')  # keep basename since we have custom actions

urlpatterns = [
    path('', include(router.urls)),
]
