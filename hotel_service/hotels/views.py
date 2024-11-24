from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Hotel
from .serializers import HotelSerializer

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated]

from .models import Booking
from .serializers import BookingSerializer

class HotelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, hotel_id):
        try:
            hotel = Hotel.objects.get(id=hotel_id)
            if hotel.available_rooms > 0:
                data = request.data
                data['hotel'] = hotel.id
                data['user_id'] = request.user.id
                data['total_price'] = (
                    (hotel.price_per_night) *
                    ((data['check_out_date'] - data['check_in_date']).days)
                )
                serializer = BookingSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    hotel.available_rooms -= 1
                    hotel.save()
                    return Response(serializer.data, status=201)
                return Response(serializer.errors, status=400)
            return Response({"error": "No rooms available."}, status=400)
        except Hotel.DoesNotExist:
            return Response({"error": "Hotel not found."}, status=404)
