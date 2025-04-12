from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomAuthToken, UserViewSet, ProfileViewSet, CategoryViewSet,
    ItemViewSet, ReviewViewSet, OrderViewSet, NotificationViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'items', ItemViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', CustomAuthToken.as_view(), name='auth_token'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]