from django.contrib import admin
from .models import CustomUser, Bus, Booking, Route

# Register Route Model with customization
@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('origin_city', 'destination_city', 'origin_latitude', 'origin_longitude', 'destination_latitude', 'destination_longitude')
    search_fields = ('origin_city', 'destination_city')
    fieldsets = (
        ('Route Information', {
            'fields': ('origin_city', 'destination_city')
        }),
        ('Origin Location', {
            'fields': ('origin_latitude', 'origin_longitude'),
            'description': 'Enter latitude and longitude for the origin city'
        }),
        ('Destination Location', {
            'fields': ('destination_latitude', 'destination_longitude'),
            'description': 'Enter latitude and longitude for the destination city'
        }),
    )

# Register Bus Model with customization
@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'seats', 'route', 'price')
    search_fields = ('name', 'owner')
    list_filter = ('owner',)
    fieldsets = (
        ('Bus Information', {
            'fields': ('name', 'owner', 'seats', 'price')
        }),
        ('Route Assignment', {
            'fields': ('route',),
            'description': 'Select a route for this bus. Routes are created in the Routes section.'
        }),
    )

# Register Booking Model with customization
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'passenger_name', 'bus', 'seats_booked', 'travel_date', 'payment_status', 'status')
    search_fields = ('passenger_name__email', 'bus__name')
    list_filter = ('payment_status', 'status', 'travel_date')
    readonly_fields = ('booking_date', 'payment_date', 'refund_date', 'cancellation_date', 'razorpay_payment_id', 'razorpay_order_id')
    fieldsets = (
        ('Booking Details', {
            'fields': ('bus', 'passenger_name', 'seats_booked', 'booking_date', 'travel_date')
        }),
        ('Location', {
            'fields': ('start_location', 'drop_location')
        }),
        ('Payment Information', {
            'fields': ('amount', 'payment_status', 'payment_date', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature')
        }),
        ('Booking Status & Refunds', {
            'fields': ('status', 'refund_id', 'refund_amount', 'refund_date', 'cancellation_date')
        }),
    )

admin.site.register(CustomUser)

