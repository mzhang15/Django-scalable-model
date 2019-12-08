from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from scalable import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'mappings', views.MappingViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
