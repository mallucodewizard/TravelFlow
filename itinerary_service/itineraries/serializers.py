from rest_framework import serializers
from .models import Itinerary, SightseeingActivity


class SightseeingActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SightseeingActivity
        fields = [
            'id',
            'itinerary_id',
            'name',
            'description',
            'start_time',
            'end_time',
            'location',
        ]



class ItinerarySerializer(serializers.ModelSerializer):
    activities = SightseeingActivitySerializer(many=True, read_only=True)

    class Meta:
        model = Itinerary
        fields = '__all__'
        extra_kwargs = {
            'user_id': {'required': False}
        }

class ItineraryDetailSerializer(serializers.ModelSerializer):
    activities = serializers.SerializerMethodField(required=False)
    def get_activities(self, obj):
        activities = SightseeingActivity.objects.filter(itinerary_id=obj.id)
        return SightseeingActivitySerializer(activities, many=True).data

    class Meta:
        model = Itinerary
        fields = '__all__'