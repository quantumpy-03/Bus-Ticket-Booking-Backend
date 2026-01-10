from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

class Route(models.Model):
    """Represents a route with static origin and destination locations"""
    origin_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    origin_latitude = models.FloatField(null=True, blank=True)
    origin_longitude = models.FloatField(null=True, blank=True)
    destination_latitude = models.FloatField(null=True, blank=True)
    destination_longitude = models.FloatField(null=True, blank=True)
    
    class Meta:
        unique_together = ('origin_city', 'destination_city')
    
    def __str__(self):
        return f"{self.origin_city} → {self.destination_city}"

class Bus(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=50)
    seats = models.IntegerField()
    route = models.ForeignKey(Route, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    BOOKING_STATUS_CHOICES = [
        ('BOOKED', 'Booked'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
    ]

    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    passenger_name = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    seats_booked = models.IntegerField()
    start_location = models.CharField(max_length=100, blank=True, null=True)
    drop_location = models.CharField(max_length=100, blank=True, null=True)
    booking_date = models.DateTimeField(auto_now_add=True)
    travel_date = models.DateField(null=True, blank=True)
    
    # Payment fields
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(null=True, blank=True)
    
    # Booking Status & Refund Fields
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='BOOKED')
    refund_id = models.CharField(max_length=100, null=True, blank=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    refund_date = models.DateTimeField(null=True, blank=True)
    cancellation_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Booking {self.id} - {self.passenger_name.email}"
    