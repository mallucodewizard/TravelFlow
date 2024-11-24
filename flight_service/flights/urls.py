from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FlightViewSet, FlightBookingView

router = DefaultRouter()
router.register(r'', FlightViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('book/<int:flight_id>/', FlightBookingView.as_view(), name='flight-book'),
]
   
