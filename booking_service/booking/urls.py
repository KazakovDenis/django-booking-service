from django.urls import path

from .views import BookingView, SuccessView

urlpatterns = [
    path('', BookingView.as_view(), name='booking'),
    path('success/', SuccessView.as_view(), name='success'),
]
