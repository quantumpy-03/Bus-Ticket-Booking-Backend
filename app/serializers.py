from rest_framework import serializers
from .models import CustomUser, Bus, Booking, Route
from datetime import date

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

# ...existing code...

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"


class BusSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    
    class Meta:
        model = Bus
        fields = "__all__"

class BookingSerializer(serializers.ModelSerializer):
    passenger_name = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, data):
        travel_date = data.get('travel_date')
        if not travel_date:
            raise serializers.ValidationError({'travel_date': 'Travel date is required.'})
        if travel_date <= date.today():
            raise serializers.ValidationError({'travel_date': 'Travel date must be in the future.'})
        return data

    class Meta:
        model = Booking
        fields = "__all__"

