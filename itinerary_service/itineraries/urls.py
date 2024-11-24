from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItineraryViewSet,SightseeingActivityViewSet

router = DefaultRouter()
router.register(r'sightseeing', SightseeingActivityViewSet, basename='sightseeing')
router.register(r'', ItineraryViewSet, basename='itinerary')
urlpatterns = [
     path('', include(router.urls)),
]


