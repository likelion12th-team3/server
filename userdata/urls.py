from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from .views import update_today_data

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("update_today/", update_today_data, name="update_today_data"),
]