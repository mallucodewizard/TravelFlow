from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Flight
from .serializers import FlightSerializer
from rest_framework import viewsets

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated]

class FlightBookingView(APIView):
    permission_classes = []

    def post(self, request, flight_id):
        try:
            flight = Flight.objects.get(id=flight_id)
            if flight.seats_available > 0:
                flight.seats_available -= 1
                flight.save()
                return Response({"message": "Flight booked successfully!"})
            return Response({"error": "No seats available."}, status=400)
        except Flight.DoesNotExist:
            return Response({"error": "Flight not found."}, status=404)
