from django.db import models

class Itinerary(models.Model):
    user_id = models.PositiveIntegerField()  # Reference to the user
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    flight_ids = models.JSONField(default=list)  # Store multiple flight IDs
    hotel_ids = models.JSONField(default=list)  # Store multiple hotel IDs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (User {self.user_id})"


class SightseeingActivity(models.Model):
    itinerary_id = models.PositiveIntegerField()  # Associates activity with an itinerary
    name = models.CharField(max_length=255)  # Name of the activity
    description = models.TextField(blank=True, null=True)  # Optional description
    start_time = models.DateTimeField()  # Start time of the activity
    end_time = models.DateTimeField()  # End time of the activity
    location = models.CharField(max_length=255)  # Location of the activity

    def __str__(self):
        return f"{self.name} (Itinerary {self.itinerary_id})"
