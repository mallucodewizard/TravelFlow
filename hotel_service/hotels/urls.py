from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, HotelBookingView

router = DefaultRouter()
router.register(r'', HotelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('book/<int:hotel_id>/', HotelBookingView.as_view(), name='hotel-book'),
]