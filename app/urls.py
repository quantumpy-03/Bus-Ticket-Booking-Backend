from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import BookingViewSet, BusViewSet, CustomUserViewSet, create_razorpay_order, verify_razorpay_payment, ProfileView, cancel_booking

router = routers.DefaultRouter()

router.register("buses", BusViewSet, basename="buses")
router.register("book", BookingViewSet, basename="book")
router.register("users", CustomUserViewSet, basename="users")

urlpatterns = [
    
    path('auth/token/', TokenObtainPairView.as_view(), name="user_login"),
    path('auth/token/refresh/', TokenRefreshView.as_view(),name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='user_profile'),

    # Payment endpoints
    path('payments/create-order/', create_razorpay_order, name='create_order'),
    path('payments/verify/', verify_razorpay_payment, name='verify_payment'),
    
    # Cancellation endpoint
    path('bookings/<int:booking_id>/cancel/', cancel_booking, name='cancel_booking'),

    path('', include(router.urls)),
]
