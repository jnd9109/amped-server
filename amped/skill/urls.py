# Create a router and register our viewsets with it.
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from skill.views import SkillViewSet

router = DefaultRouter()
router.register(r'', SkillViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
