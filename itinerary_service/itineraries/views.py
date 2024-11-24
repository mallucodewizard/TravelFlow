from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Itinerary, SightseeingActivity
from .serializers import ItinerarySerializer, SightseeingActivitySerializer, ItineraryDetailSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Itinerary
from .serializers import ItinerarySerializer

class ItineraryViewSet(viewsets.ModelViewSet):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Itinerary.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ItineraryDetailSerializer
        return ItinerarySerializer

# import requests
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .models import Itinerary

# class AddFlightToItineraryView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, itinerary_id):
#         flight_id = request.data.get('flight_id')
#         if not flight_id:
#             return Response({"error": "flight_id is required"}, status=400)

#         try:
#             itinerary = Itinerary.objects.get(id=itinerary_id, user_id=request.user.id)

#             # Avoid duplicate entries
#             if flight_id in itinerary.flight_ids:
#                 return Response({"message": "Flight already added to itinerary."}, status=200)

#             itinerary.flight_ids.append(flight_id)
#             itinerary.save()
#             return Response({"message": "Flight added to itinerary successfully."}, status=201)
#         except Itinerary.DoesNotExist:
#             return Response({"error": "Itinerary not found or access denied."}, status=404)

# class AddHotelToItineraryView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, itinerary_id):
#         hotel_id = request.data.get('hotel_id')
#         if not hotel_id:
#             return Response({"error": "hotel_id is required"}, status=400)

#         try:
#             itinerary = Itinerary.objects.get(id=itinerary_id, user_id=request.user.id)

#             # Avoid duplicate entries
#             if hotel_id in itinerary.hotel_ids:
#                 return Response({"message": "Hotel already added to itinerary."}, status=200)

#             itinerary.hotel_ids.append(hotel_id)
#             itinerary.save()
#             return Response({"message": "Hotel added to itinerary successfully."}, status=201)
#         except Itinerary.DoesNotExist:
#             return Response({"error": "Itinerary not found or access denied."}, status=404)


# class FetchFullItineraryView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, itinerary_id):
#         try:
#             itinerary = Itinerary.objects.get(id=itinerary_id, user_id=request.user.id)

#             # Fetch flight details from Flight Service
#             flights = []
#             for flight_id in itinerary.flight_ids:
#                 flight_service_url = f"http://flight-service/api/flights/{flight_id}/"
#                 response = requests.get(
#                     flight_service_url,
#                     headers={"Authorization": f"Bearer {request.auth}"}
#                 )
#                 if response.status_code == 200:
#                     flights.append(response.json())

#             # Fetch hotel details from Hotel Service
#             hotels = []
#             for hotel_id in itinerary.hotel_ids:
#                 hotel_service_url = f"http://hotel-service/api/hotels/{hotel_id}/"
#                 response = requests.get(
#                     hotel_service_url,
#                     headers={"Authorization": f"Bearer {request.auth}"}
#                 )
#                 if response.status_code == 200:
#                     hotels.append(response.json())

#             # Fetch local sightseeing activities
#             activities = SightseeingActivity.objects.filter(itinerary_id=itinerary_id)
#             activity_serializer = SightseeingActivitySerializer(activities, many=True)

#             return Response({
#                 "itinerary": {
#                     "id": itinerary.id,
#                     "name": itinerary.name,
#                     "start_date": itinerary.start_date,
#                     "end_date": itinerary.end_date,
#                     "flights": flights,
#                     "hotels": hotels,
#                     "activities": activity_serializer.data,
#                 }
#             })
#         except Itinerary.DoesNotExist:
#             return Response({"error": "Itinerary not found or access denied."}, status=404)
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# from .models import Itinerary
# from .serializers import ItinerarySerializer

# class CreateItineraryView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         """
#         Create a new itinerary for the authenticated user.
#         """
#         data = request.data
#         data['user_id'] = request.user.id  # Associate the itinerary with the authenticated user
#         serializer = ItinerarySerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {"message": "Itinerary created successfully.", "data": serializer.data},
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(
#             {"message": "Validation failed.", "errors": serializer.errors},
#             status=status.HTTP_400_BAD_REQUEST
#         )

# from .models import SightseeingActivity
# from .serializers import SightseeingActivitySerializer

class CreateSightseeingActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, itinerary_id):
        """
        Add a sightseeing activity to an existing itinerary.
        """
        data = request.data
        data['itinerary_id'] = itinerary_id  # Associate the activity with the itinerary
        serializer = SightseeingActivitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Sightseeing activity added successfully.", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "Validation failed.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import SightseeingActivity
from .serializers import SightseeingActivitySerializer

class SightseeingActivityViewSet(ModelViewSet):
    """
    A ViewSet for managing sightseeing activities.
    """
    queryset = SightseeingActivity.objects.all()
    serializer_class = SightseeingActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter sightseeing activities by itinerary_id.
        """
        itinerary_id = self.request.query_params.get('itinerary_id')
        if itinerary_id:
            return self.queryset.filter(itinerary_id=itinerary_id)
        return self.queryset

    def create(self, request, *args, **kwargs):
        """
        Override create to associate the activity with an itinerary.
        Extract itinerary_id from request.data.
        """
        data = request.data
        itinerary_id = data.get('itinerary_id')
        if not itinerary_id:
            return Response(
                {"error": "itinerary_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Sightseeing activity added successfully.", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "Validation failed.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
