from django.urls import path

from . import views

urlpatterns = [
    path('', views.BookingView.as_view(), name='booking'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('schedule/<int:id>', views.doctor_appointments_view, name='schedule'),
]
