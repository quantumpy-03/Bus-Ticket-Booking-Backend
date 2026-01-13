from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Bus, Booking, CustomUser, Route
from .serializers import BusSerializer, BookingSerializer, CustomUserSerializer, RouteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import api_view, permission_classes, action
import razorpay
import hashlib
import hmac
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['origin_city', 'destination_city']
    ordering_fields = ['origin_city', 'destination_city']

class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'owner', 'route__origin_city', 'route__destination_city']
    ordering_fields = ['name', 'seats']

    def get_queryset(self):
        origin = self.request.query_params.get('origin_city')
        destination = self.request.query_params.get('destination_city')
        
        queryset = Bus.objects.all()
        
        if origin and destination:
            queryset = queryset.filter(
                route__origin_city=origin,
                route__destination_city=destination
            )
        
        return queryset


class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(passenger_name=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(passenger_name=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer



# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_razorpay_order(request):
    """Create a Razorpay order for payment processing"""
    try:
        booking_id = request.data.get('booking_id')
        amount = request.data.get('amount')
        currency = request.data.get('currency', 'INR')

        if not booking_id or not amount:
            return Response(
                {'error': 'booking_id and amount are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify booking exists and belongs to user
        try:
            booking = Booking.objects.get(id=booking_id, passenger_name=request.user)
        except Booking.DoesNotExist:
            return Response(
                {'error': 'Booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Create Razorpay order
        razorpay_order = razorpay_client.order.create({
            'amount': int(amount * 100),  # Convert to paise
            'currency': currency,
            'notes': {
                'booking_id': str(booking_id),
                'user_email': request.user.email,
            }
        })

        # Save order ID to booking
        booking.razorpay_order_id = razorpay_order['id']
        booking.amount = amount
        booking.save()

        return Response({
            'razorpay_order_id': razorpay_order['id'],
            'amount': amount,
            'currency': currency,
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {'error': f'Failed to create order: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_razorpay_payment(request):
    """Verify Razorpay payment signature and confirm booking"""
    try:
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_signature = request.data.get('razorpay_signature')

        if not all([razorpay_payment_id, razorpay_order_id, razorpay_signature]):
            return Response(
                {'error': 'Missing payment details'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Find booking by order ID
        try:
            booking = Booking.objects.get(
                razorpay_order_id=razorpay_order_id,
                passenger_name=request.user
            )
        except Booking.DoesNotExist:
            return Response(
                {'error': 'Booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Verify signature
        message = f'{razorpay_order_id}|{razorpay_payment_id}'
        expected_signature = hmac.new(
            settings.RAZORPAY_SECRET_KEY.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()

        if razorpay_signature != expected_signature:
            booking.payment_status = 'failed'
            booking.save()
            return Response(
                {'error': 'Payment verification failed'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Payment verified successfully
        booking.razorpay_payment_id = razorpay_payment_id
        booking.razorpay_signature = razorpay_signature
        booking.payment_status = 'completed'
        booking.payment_date = timezone.now()
        booking.save()

        # Update bus seats
        bus = booking.bus
        bus.seats -= booking.seats_booked
        bus.save()

        return Response({
            'message': 'Payment verified successfully',
            'booking_id': booking.id,
            'payment_status': booking.payment_status,
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': f'Payment verification failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_booking(request, booking_id):
    """Cancel a booking and initiate refund"""
    try:
        # Verify booking exists and belongs to user
        try:
            booking = Booking.objects.get(id=booking_id, passenger_name=request.user)
        except Booking.DoesNotExist:
            return Response(
                {'error': 'Booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if booking can be cancelled
        if booking.status != 'BOOKED':
            return Response(
                {'error': f'Booking is already {booking.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if booking.payment_status != 'completed':
            return Response(
                {'error': 'Only completed payments can be refunded'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate refund amount based on cancellation timing
        hours_before_departure = (booking.travel_date - timezone.now().date()).days * 24
        hours_before_departure += (booking.travel_date.hour - timezone.now().hour) if hours_before_departure == 0 else 0
        
        if hours_before_departure > 24:
            refund_percentage = 0.80  # 80% refund if cancelled >24h before
        elif hours_before_departure > 12:
            refund_percentage = 0.50  # 50% refund if cancelled 12-24h before
        else:
            refund_percentage = 0.25  # 25% refund if cancelled <12h before
        
        refund_amount = float(booking.amount) * refund_percentage
        
        # Initiate Razorpay refund
        try:
            refund_response = razorpay_client.payment.refund(
                booking.razorpay_payment_id,
                {
                    'amount': int(refund_amount * 100),  # Convert to paise
                    'notes': {
                        'booking_id': str(booking_id),
                        'reason': 'Customer cancellation'
                    }
                }
            )
            
            refund_id = refund_response['id']
        except Exception as refund_error:
            return Response(
                {'error': f'Failed to process refund: {str(refund_error)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Update booking status
        booking.status = 'CANCELLED'
        booking.refund_id = refund_id
        booking.refund_amount = refund_amount
        booking.refund_date = timezone.now()
        booking.cancellation_date = timezone.now()
        booking.save()
        
        # Release seats back to the bus
        bus = booking.bus
        bus.seats += booking.seats_booked
        bus.save()
        
        return Response({
            'message': 'Booking cancelled successfully',
            'booking_id': booking.id,
            'refund_id': refund_id,
            'refund_amount': refund_amount,
            'status': 'CANCELLED'
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': f'Cancellation failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

