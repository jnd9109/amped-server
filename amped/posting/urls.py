# Create a router and register our viewsets with it.
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posting.views import PostingViewSet

router = DefaultRouter()
router.register(r'', PostingViewSet, basename='posting')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
