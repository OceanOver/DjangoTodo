""" URL Configuration
"""
from django.urls import path, include
from rest_framework import routers
from .user.views import UserViewSet, login, register, upload
from .task.views import ItemViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'user', UserViewSet)
router.register(r'item', ItemViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login', login),
    path('register', register),
    path('upload', upload),
]
